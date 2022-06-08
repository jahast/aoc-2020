open System
open System.IO
open Microsoft.FSharp.Core

// yeah this is pretty terrible
let input =
    File.ReadAllLines("./input.txt") |> Array.toList

let split s = s |> List.ofSeq |> List.map string

type Operator =
    | Sum
    | Multiply

type Token =
    | Value of uint64
    | Operator of Operator
    | Open
    | Close

type Expr =
    | Literal of uint64
    | Bracketed of Expr * Operator * Expr
    | Normal of Expr * Operator * Expr
    | Empty

let tryParse (x: string) =
    match Int32.TryParse x with
    | true, int -> Some int
    | _ -> None

let tokenize str =
    let splat = str |> split |> List.filter ((<>) " ")

    splat
    |> List.map<string, Token>
        (fun (x: string) ->
            match x with
            | "*" -> Operator(Multiply)
            | "+" -> Operator(Sum)
            | "(" -> Open
            | ")" -> Close
            | _ ->
                let parsed = tryParse x

                match parsed with
                | Some value -> Value(uint64 value)
                | None -> failwithf "no gut")

let mid xs =
    let len = List.length xs
    xs.[1..(len - 2)]

let isolate tokens =
    let _, Some i =
        tokens
        |> List.indexed
        |> List.fold
            (fun state (i, tok) ->
                let acc, found = state

                match found, tok with
                | Some _, _ -> state
                | _, Close -> (acc + 1, found)
                | _, Open ->
                    if acc = 1 then
                        (acc, Some(i))
                    else
                        (acc - 1, None)
                | _, _ -> state)
            (0, None)

    let before, after = tokens |> List.splitAt (i + 1)
    (mid before, after)

let pars (inputTokens: Token list) =
    let rec inner (tokens: Token list) =
        if (List.length tokens) = 0 then
            Empty, []
        else
            let x::xs = tokens

            match x with
            | Value i ->
                match xs with
                | [] -> Literal i, []
                | operator :: afterOperator ->
                    let operatorExpression =
                        if operator = Operator(Sum) then
                            Sum
                        else
                            Multiply

                    match afterOperator with
                    | [] -> Normal(Empty, operatorExpression, Literal i), []
                    | [ Value j ] -> Normal(Literal j, operatorExpression, Literal i), []
                    | _ ->
                        let left, afterLeft = inner afterOperator
                        Normal(left, operatorExpression, Literal i), afterLeft
            | Close ->
                let rightTokens, afterRightTokens = isolate tokens
                let right, _ = inner rightTokens

                match afterRightTokens with
                | [] -> right, []
                | _ ->
                    let operator::afterOperator = afterRightTokens

                    let operatorExpression =
                        if operator = Operator(Sum) then
                            Sum
                        else
                            Multiply

                    let left, afterLeft = inner afterOperator
                    Bracketed(left, operatorExpression, right), afterLeft

    let res, _ = inputTokens |> List.rev |> inner
    res

let expressions = input |> List.map (tokenize >> pars)

let rec visit (e: Expr) =
    match e with
    | Literal i -> int64 i
    | Normal (left, operator, right) ->
        let l, r = visit left, visit right

        match operator with
        | Sum -> l + r
        | Multiply -> l * r
    | Bracketed (left, operator, right) ->
        let r, l = visit right, visit left

        match operator with
        | Sum -> l + r
        | Multiply -> l * r

expressions
|> List.map visit
|> List.sum
|> printfn "%A"

let reduce (inputTokens: Token list) =
    let reduceSums (tokens: Token list) =
        let sumMatch =
            tokens
            |> List.windowed 3
            |> List.indexed
            |> List.tryPick
                (fun (i, win) ->
                    match win with
                    | [ (Value j); Operator (Sum); (Value k) ] -> Some(i, Value(k + j))
                    | _ -> None)

        let asd =
            match sumMatch with
            | None -> []
            | Some value -> [ value ]

        asd
        |> List.fold
            (fun state (i, v) ->
                state
                |> List.removeManyAt i 3
                |> List.insertAt i v)
            tokens

    let reduceMults (tokens: Token list) =
        let multMatches =
            tokens
            |> List.windowed 5
            |> List.indexed
            |> List.tryPick
                (fun (i, win) ->
                    match win with
                    | [ Open; (Value j); Operator (Multiply); (Value k); Close ] -> Some(i, Value(k * j))
                    | _ -> None)

        let asd =
            match multMatches with
            | None -> []
            | Some value -> [ value ]

        asd
        |> List.fold
            (fun state (i, v) ->
                state
                |> List.removeManyAt i 5
                |> List.insertAt i v)
            tokens

    let rec reduceBrackets (tokens: Token list) =
        let matches =
            tokens
            |> List.windowed 3
            |> List.indexed
            |> List.tryPick
                (fun (i, win) ->
                    match win with
                    | [ Open; Value j; Close ] -> Some(i, Value(j))
                    | _ -> None)

        let asd =
            match matches with
            | None -> []
            | Some value -> [ value ]
        
        asd
        |> List.fold
            (fun state (i, v) ->
                state
                |> List.removeManyAt i 3
                |> List.insertAt i v)
            tokens

    let rec reduceLol (tokens: Token list) =
        let matches =
            tokens
            |> List.windowed 4
            |> List.indexed
            |> List.choose
                (fun (i, win) ->
                    match win with
                    | [ Open; Value j; Operator (Multiply); Value k ] -> Some(i, [ Open; Value(j * k) ])
                    | _ -> None)

        let asd =
            match matches with
            | [] -> []
            | xs -> [List.last xs]
        
        asd
        |> List.fold
            (fun state (i, v) ->
                state
                |> List.removeManyAt i 4
                |> List.insertManyAt i v)
            tokens

    let rec yesIKnow (tokens: Token list) =
        let hasSum = tokens |> List.contains (Operator(Sum))

        if hasSum then
            tokens
        else
            let matches =
                tokens
                |> List.windowed 3
                |> List.indexed
                |> List.tryPick
                    (fun (i, win) ->
                        match win with
                        | [ Value k; Operator Multiply; Value j ] -> Some(i, Value(j * k))
                        | _ -> None)

            let asd =
                match matches with
                | None -> []
                | Some value -> [ value ]

            asd
            |> List.fold
                (fun state (i, v) ->
                    state
                    |> List.removeManyAt i 3
                    |> List.insertAt i v)
                tokens

    let rec inner (tokens: Token list) =
        match tokens with
        | [ Value i ] -> i
        | [ (Value j); Operator (Multiply); (Value k) ] -> j * k
        | _ ->
            let reduced =
                tokens
                |> reduceSums
                |> reduceMults
                |> reduceBrackets

            if (List.length reduced) = (List.length tokens) then
                let asd = reduced |> reduceLol

                if (List.length asd) = (List.length reduced) then
                    asd |> yesIKnow |> inner
                else
                    asd |> inner
            else
                reduced |> inner

    inner inputTokens

//57052941475865 low
//6731717832000
//19726226016480
//259727391000
//364320520200
//267478848000
//102371623200
//159330084000
//27968663345210

let test = "4 * 2 + (4 + 5 + (3 + 5 + 9) + 7 + 7 + 4) + 3 + (6 * (2 + 2 + 8 * 8) + (8 + 9 * 7 + 7 + 6 * 9) + (3 * 9 * 3 * 5 + 5) * 5) * 3"

test |> tokenize |> reduce |> printfn "%A"

input |> List.map (tokenize >> reduce) |> List.sum |> printf "%A"
