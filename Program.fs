module Prog
open AJson

type 'a testRecord =
    {
        x : 'a;
        y : int array
        c : option<int>
    }

type S<'a> =
    | S1 of 'a
    | S2 of string * 'a
    | S3 of S<'a> array
    | S4 of 'a list
    | S5 of int8 array * S<'a>  list



[<EntryPoint>]
let test _ =
    printfn "%A" <| deserialize<int testRecord> "{\"x\": 2, \"y\": [3, 5, 6], \"c\": null}"
    printfn "%A" <| deserialize<int testRecord> "{\"x\": 100, \"y\": [], \"c\": 10}"
    printfn "%A" <| deserialize<int testRecord> "{\"x\": 100, \"y\": [], \"c\": 10}"

    let x = "{\"_TAG\": \"S1\", \"_VALUES\": [3]}"
    printfn "%A" <| deserialize<S<int>> x

    let r = deserialize<int testRecord> "{\"x\": 100, \"y\": [], \"c\": 10}"

    let s1 = S1 r
    let s2 = S2 ("string", r)
    let s3 = S3 [|s1; s2|]
    let s4 = S4 [r; r]
    let s5 = S5 ([|sbyte 2|], [s1; s2; s3; s4])

    let s = serialize s5
    printfn "%s" s

    let d = deserialize<S<testRecord<int>>> s
    printfn "%A" (d = s5)
    0
