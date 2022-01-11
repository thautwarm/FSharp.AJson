module AJson
open Microsoft.FSharp.Reflection

type Json =
        | JInt of int64
        | JFloat of double
        | JBool of bool
        | JStr of string
        | JNull
        | JList of Json ResizeArray
        | JDict of (string * Json) ResizeArray
    with
     member this.kind =
        match this with
        | JInt _ -> "int"
        | JFloat _ -> "float"
        | JBool _ -> "bool"
        | JStr _ -> "string"
        | JNull _ -> "null"
        | JList _ -> "list"
        | JDict _ -> "dict"

module Parsec =
    type Parser<'a> = int -> string -> int * 'a
    let pChar_ (c: char) =
        let apply (i: int) (s: string) =
            if i >= s.Length || s.[i] <> c then invalidOp "unexpected match"
            else (i + 1, ())
        apply

    let pStr_ (pat: string) =
        let apply (i: int) (s: string) =

            if i + pat.Length > s.Length || s.[i..i+pat.Length - 1] <> pat then invalidOp "unexpected match"
            else (i + pat.Length, ())
        apply

    let pChar (c: char) =
        let apply (i: int) (s: string) =
            if i >= s.Length || s.[i] <> c then invalidOp "unexpected match"
            else (i + 1, c)
        apply

    let pCharset_ (cs : char array) =
        let apply (i: int) (s: string) =
            if i >= s.Length then invalidOp "unexpected match"
            elif Array.contains s.[i] cs then (i+1, ())
            else invalidOp "unexpected match"
        apply

    let pCharset (cs : char array) =
        let apply (i: int) (s: string) =
            if i >= s.Length then invalidOp "unexpected match"
            elif Array.contains s.[i] cs then (i+1, s.[i])
            else invalidOp $"unexpected match {s.[i]}"
        apply

    let pIgnore (p: Parser<'a>) : Parser<unit> =
        let apply i s =
            let i, _ = p i s
            (i, ())
        apply

    let pSeq_ (ps: Parser<unit> list): Parser<unit> =
        let apply (i: int) (s: string) =
            let rec loop i ps =
                if i >= s.Length then invalidOp "unexpected match"
                else
                match ps with
                | hd::tl ->
                    let i, _ =  hd i s
                    loop i tl
                | [] -> i, ()
            loop i ps
        apply

    let pSepRep (sep: Parser<bool>) (p: Parser<'a>): Parser<'a ResizeArray> =
        let apply (i: int) (s: string) =
            let res = ResizeArray<'a>()
            let rec loop i =
                if i >= s.Length then invalidOp "unexpected match"
                else
                let i, v = p i s
                res.Add(v)
                let i, test = sep i s
                if test then loop i
                else i, res
            loop i
        apply

    let pSpc : Parser<unit> =
        let apply (i: int) (s: string) =
            let rec loop i =
                if i >= s.Length then i, ()
                else
                match s.[i] with
                | ' ' | '\n' | '\r' | '\t' -> loop (i + 1)
                | _ -> i, ()
            loop i
        apply


    let allowSPC (p: Parser<'a>): Parser<'a> =
        let apply (i: int) (s: string) =
            let i, _ = pSpc i s
            let i, v = p i s
            let i, _ = pSpc i s
            i, v
        apply

    let la1 (dispatch: char -> Parser<'a>): Parser<'a> =
        let apply (i: int) (s: string) =
            if i >= s.Length then invalidOp "unexpected match"
            let p = dispatch(s.[i])
            p i s
        apply

    let pNumber : Parser<string> =
        let apply (i: int) (s: string) =
            if i >= s.Length then invalidOp "unexpected match"
            let start = i
            let rec loop j =
                if j >= s.Length then j
                else
                match s.[j] with
                | '.' | 'E' | 'e' | '-' -> loop (j + 1)
                | c when c <= '9'  && c >= '0' -> loop (j + 1)
                | _ -> j
            let i = loop i
            i, s.[start..i-1]
        apply

    let pStr : Parser<string> =
        let apply (i: int) (s: string) =
            if i >= s.Length || s.[i] <> '"' then
                invalidOp $"imcomplete parsing for string"
            let buf = System.Text.StringBuilder()
            let mutable find_end = false
            let mutable i = i + 1
            while i < s.Length && not find_end do
                match s.[i] with
                | '\\' ->
                    if i + 1 >= s.Length then
                        invalidOp $"incomplete escape for string"
                    else
                    match s.[i + 1] with
                    | 'b' -> ignore(buf.Append('\b'))
                    | 't' -> ignore(buf.Append('\t'))
                    | 'n' -> ignore(buf.Append('\n'))
                    | 'r' -> ignore(buf.Append('\r'))
                    | 'f' -> ignore(buf.Append('\f'))
                    | '\\' -> ignore(buf.Append('\\'))
                    | '"' -> ignore(buf.Append('"'))
                    | a -> ignore(buf.Append(a))
                    i <- i + 2
                | '"' ->
                    find_end <- true
                    i <- i + 1
                | a ->
                    ignore(buf.Append(a))
                    i <- i + 1
            if find_end then
                i, buf.ToString()
            else
                invalidOp "incomplete string"
        apply

    let pMap (f: 'a -> 'b) (p: Parser<'a>) : Parser<'b> =
        let apply i s =
            let i, v = p i s
            i, f v
        apply
    let pRef (p: Parser<'a> ref): Parser<'a> =
        let apply i s = p.Value i s
        apply

    module Json =
        let pListSep =
            pCharset [|','; ']'|]
            |> pMap (function
                | ',' -> true
                | ']' -> false
                | _ -> failwith "impossible")

        let pDictSep =
            pCharset [|','; '}'|]
            |> pMap (function
                | ',' -> true
                | '}' -> false
                | _ -> failwith "impossible")

        let jInt: Parser<int64> = pNumber |> pMap (fun s -> System.Int64.Parse(s))
        let jFloat: Parser<double> = pNumber |> pMap (fun s -> System.Double.Parse(s))

        let jNumber : Parser<Json> =
            let apply (i: int) (s: string) =
                if i >= s.Length then invalidOp "unexpected match"
                let start = i
                let rec loop isfloat j =
                    if j >= s.Length then isfloat, j
                    else
                    match s.[j] with
                    | '.' -> loop true (j + 1)
                    | 'E' | 'e' | '-' -> loop isfloat (j + 1)
                    | c when c <= '9'  && c >= '0' -> loop isfloat (j + 1)
                    | _ -> isfloat, j
                let isfloat, i = loop false i
                let o =
                    if isfloat then
                        JFloat(System.Double.Parse(s.[start..i-1]))
                    else
                        JInt(System.Int64.Parse(s.[start..i-1]))
                i, o
            apply

        let jTrue: Parser<bool> =
            pStr_ "true" |> pMap (fun s -> true)
        let jFalse: Parser<bool> =
            pStr_ "false" |> pMap (fun s -> true)
        let jNull: Parser<unit> = pStr_ "null"
        let jStr: Parser<string> = pStr

        let refObject: Parser<(string * Json) ResizeArray> ref = ref (Unchecked.defaultof<_>)
        let jObject = pRef refObject
        let refList: Parser<Json ResizeArray> ref = ref (Unchecked.defaultof<_>)
        let jList = pRef refList

        let json =
            la1 <| function
            | '[' -> jList |> pMap JList
            | '{' -> jObject |> pMap JDict
            | 't' -> jTrue |> pMap JBool
            | 'f' -> jFalse |> pMap JBool
            | 'n' -> jNull |> pMap (fun () -> JNull)
            | '-' -> jNumber
            | c when c >= '0' && c <= '9' -> jNumber
            | '"' -> jStr |> pMap JStr
            | c -> invalidOp (string c)


        refObject.Value <-
            fun (i: int) (s: string) ->
                let i, _ = pChar_ '{' i s
                let i, _ = pSpc i s
                if i >= s.Length then invalidOp "incomplete object"
                if s.[i] = '}' then i+1, ResizeArray<string * Json>()
                else
                let each i s =
                    let i, key = allowSPC jStr i s
                    let i, _ = allowSPC (pChar_ ':') i s
                    let i, v = allowSPC json i s
                    i, (key, v)
                pSepRep pDictSep each i s

        refList.Value <-
            fun (i: int) (s: string) ->
                let i, _ = pChar_ '[' i s
                let i, _ = pSpc i s
                if i >= s.Length then invalidOp "incomplete list"
                if s.[i] = ']' then i+1, ResizeArray<Json>()
                else
                pSepRep pListSep (allowSPC json) i s

let parseJson s =
    let i, o = (Parsec.allowSPC Parsec.Json.json) 0 s
    if i <> s.Length then invalidOp "json parse incomplete"
    else o


let int64FromJson =
    function
    | JInt i -> i
    | _ -> invalidOp "invalid conversion to int"

let doubleFromJson =
    function
    | JFloat f -> f
    | _ -> invalidOp "invalid conversion to float"

let boolFromJson =
    function
    | JBool b -> b
    | _ -> invalidOp "invalid conversion to bool"

let stringFromJson =
    function
    | JStr s -> s
    | _ -> invalidOp "invalid conversion to bool"

let charFromJson =
    function
    | JStr s when s.Length <> 1 -> invalidOp $"invalid interpretaion from string to char"
    | JStr s -> s.[0]
    | _ -> invalidOp "invalid conversion to bool"


let unitFromJson =
    function
    | JInt 0L -> ()
    | _ -> invalidOp "invalid conversion to unit"


let inline forI f (seq: ResizeArray<'a>) =
    for i = 0 to seq.Count - 1 do
        f i (seq.[i])

let inline (==) a b = obj.ReferenceEquals(a, b)

let ADT_TAG = "_TAG"
let ADT_VALS = "_VALUES"

type 'a evidence = Evidence

let rec inline fromJson<'a> data =
    unbox<'a> (objFromJson (typeof<'a>) data)

and objFromJson (t: System.Type) (data: Json) =
    if obj.ReferenceEquals(typeof<int>, t) then
        box <| int (int64FromJson data)
    elif obj.ReferenceEquals(typeof<int16>, t) then
        box <| int16 (int64FromJson data)
    elif obj.ReferenceEquals(typeof<int8>, t) then
        box <| int8 (int64FromJson data)
    elif obj.ReferenceEquals(typeof<int64>, t) then
        box <| (int64FromJson data)
    elif obj.ReferenceEquals(typeof<int8>, t) then
        box <| int8 (int64FromJson data)
    elif obj.ReferenceEquals(typeof<float>, t) then
        box <| float (doubleFromJson data)
    elif obj.ReferenceEquals(typeof<double>, t) then
        box <| (doubleFromJson data)
    elif obj.ReferenceEquals(typeof<bool>, t) then
        box <| (boolFromJson data)
    elif obj.ReferenceEquals(typeof<char>, t) then
        let s = stringFromJson data
        if s.Length <> 1 then invalidOp $"{s} to char"
        else
            box <| s.[0]
    elif obj.ReferenceEquals(typeof<string>, t) then
        box <| stringFromJson data
    elif t.IsArray then
        let eltype = t.GetElementType()
        let seq =
            match data with
            | JList seq -> seq
            | _ -> invalidOp $"convert {data.kind} to {t}"
        // integers
        if eltype == typeof<int> then
            box <| Array.init seq.Count (fun i -> int (int64FromJson seq.[i]))
        elif eltype == typeof<int64> then
            box <| Array.init seq.Count (fun i -> (int64FromJson seq.[i]))
        elif eltype == typeof<int16> then
            box <| Array.init seq.Count (fun i -> int16 (int64FromJson seq.[i]))
        elif eltype == typeof<int8> then
            box <| Array.init seq.Count (fun i -> int8 (int64FromJson seq.[i]))
        elif eltype == typeof<uint32> then
            box <| Array.init seq.Count (fun i -> Core.Operators.uint32 (int64FromJson seq.[i]))
        elif eltype == typeof<uint64> then
            box <| Array.init seq.Count (fun i -> Core.Operators.uint64 (int64FromJson seq.[i]))
        elif eltype == typeof<uint8> then
            box <| Array.init seq.Count (fun i -> Core.Operators.byte (int64FromJson seq.[i]))
        elif eltype == typeof<uint16> then
            box <| Array.init seq.Count (fun i -> Core.Operators.uint16 (int64FromJson seq.[i]))

        // floats
        elif eltype == typeof<float> then
            box <| Array.init seq.Count (fun i -> float (doubleFromJson seq.[i]))
        elif eltype == typeof<double> then
            box <| Array.init seq.Count (fun i -> (doubleFromJson seq.[i]))
        elif eltype == typeof<decimal>  then
            box <| Array.init seq.Count (fun i -> decimal (doubleFromJson seq.[i]))
        // others
        elif eltype == typeof<string> then
            box <| Array.init seq.Count (fun i -> (stringFromJson seq.[i]))
        elif eltype == typeof<bool> then
            box <| Array.init seq.Count (fun i -> (boolFromJson seq.[i]))
        elif eltype == typeof<unit> then
            box <| Array.init seq.Count (fun i -> (unitFromJson seq.[i]))
        elif eltype == typeof<char> then
            box <| Array.init seq.Count (fun i -> (charFromJson seq.[i]))
        else
            box <| Array.init seq.Count (fun i -> objFromJson eltype seq.[i])
        // let array = System.Array.CreateInstance(eltype, seq.Count)
        // for i = 0 to seq.Count - 1 do
        //     array.SetValue(objFromJson eltype (seq.[i]), i)
        // box <| array
    elif t.IsGenericType && t.GetGenericTypeDefinition() = typedefof<option<_>> then
        let eltype = t.GenericTypeArguments.[0]
        match data with
        | JNull -> None: obj
        | _ -> Some (objFromJson eltype data)
    elif t.IsGenericType && t.GetGenericTypeDefinition() = typedefof<list<_>> then
        let eltype = t.GenericTypeArguments.[0]
        let mutable o: obj list = []
        let seq =
            match data with
            | JList seq -> seq
            | _ -> invalidOp $"convert {data.kind} to {t}"
        for i = seq.Count - 1 downto 0 do
            o <- objFromJson eltype seq.[i] :: o
        box <| o
    elif FSharpType.IsRecord t then
        let fields = FSharpType.GetRecordFields t
                     |> Array.map (fun f -> f.Name, f.PropertyType)
        let arguments = Array.create fields.Length (null: obj)
        let pairs =
            match data with
            | JDict pairs -> pairs
            | _ -> invalidOp $"convert {data.kind} to {t}"
        for (k, v) in pairs do
            let i = Array.findIndex (fun (fname, _) -> k = fname) fields
            let (_, fieldt) = fields.[i]
            arguments.[i] <- objFromJson fieldt v
        FSharpValue.MakeRecord(t, arguments)
    elif FSharpType.IsTuple t then
        let eltypes = FSharpType.GetTupleElements t
        let seq =
            match data with
            | JList seq -> seq
            | _ -> invalidOp $"convert {data.kind} to {t}"
        FSharpValue.MakeTuple(
            Array.init seq.Count (fun i -> objFromJson eltypes.[i] seq.[i]), t)
    elif FSharpType.IsUnion t then
        let pairs =
            match data with
            | JDict pairs -> pairs
            | _ -> invalidOp $"convert {data.kind} to {t}"
        let _, tag = Seq.find (fun (k, _) -> k = ADT_TAG) pairs
        let tag = stringFromJson tag
        let _, values = Seq.find (fun (k, _) -> k = ADT_VALS) pairs
        let case =
            FSharpType.GetUnionCases t
            |> Array.find (fun case -> case.Name = tag)
        let fieldtypes = case.GetFields() |> Array.map (fun f -> f.PropertyType)
        let values =
            match values with
            | JList values -> Array.init values.Count (fun i -> objFromJson fieldtypes.[i] values.[i])
            | _ -> invalidOp $"convert {data.kind} to {t}"
        FSharpValue.MakeUnion(case, values)
    else
        invalidOp $"unsupported data type fromJson: {t}"


#if FABLE_COMPILER

let inline deserialize<'a> s =
    let json = parseJson s
    objFromJson typeof<'a> json :?> 'a

#else

let inline deserialize<'a> s = FSharp.Json.Json.deserialize<'a> s

#endif