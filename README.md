# FSharp.AJson

F# Json serialization/deserialization for algebriac data types and nominal records; compatible to Fable's existing backends

This parser has been already tested against a large and real-world JSON file: https://github.com/thautwarm/parser-data 

## Usage

To load JSON configuations in F\#, no matter which codegen target(.NET, JS, Python, etc) is used.

```F#

type S<'a> =
    | S1 of 'a
    | S2 of string * 'a
    | S3 of S<'a> array
    | S4 of 'a list
    | S5 of int8 array * 'a
    
let x = "{\"_TAG\": \"S1\", \"_VALUES\": [3]}"
    printfn "%A" <| deserialize<S<int>> x (* S1 1 *)
```

## Features

```F#
type Json =
        | JNull
        | JInt of int64
        | JFloat of double
        | JBool of bool
        | JStr of string
        | JList of Json ResizeArray
        | JDict of (string * Json) ResizeArray
```

- [ ] To be complelete, it can be slow. Hence, you might consider alternatives when JSON parsing is the performance bottleneck.
- [x] Parsing raw JSON data: `AJson.parseJson: string -> Json`
- [ ] deserializing/serializing records and ADTs like that in [FSharp.Json](https://github.com/vsapronov/FSharp.Json):
   - [ ] `AJson.serialize any`
   - [x] `AJson.deserialize<MyType> str`
   

## Motivation

I need a package manager(as well as a project builder) to manage F\# dependencies and PyPI dependencies for my master-thesis project [Typed BNF](https://github.com/thautwarm/typed-bnf),

which requires me to implement a usable package manager for the Fable Python backend(this is the easy approach),

which requires me to implement a type-safe JSON deserialization/serialization for accessing PyPI APIs and project configuration files,

which requires me to implement this project.



