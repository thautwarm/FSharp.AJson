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
    | S5 of int8 array * 'a
    


[<EntryPoint>]
let test _ =
    printfn "%A" <| deserialize<int testRecord> "{\"x\": 2, \"y\": [3, 5, 6], \"c\": null}"
    printfn "%A" <| deserialize<int testRecord> "{\"x\": 100, \"y\": [], \"c\": 10}"
    printfn "%A" <| deserialize<int testRecord> "{\"x\": 100, \"y\": [], \"c\": 10}"
    
    let x = "{\"_TAG\": \"S1\", \"_VALUES\": [3]}"
    printfn "%A" <| deserialize<S<int>> x
    0

