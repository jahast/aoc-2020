open System.IO

let split s = s |> List.ofSeq |> List.map string

let input =
    File.ReadAllLines("./input.txt")
    |> Array.toList
    |> List.map split

let initialCoords =
    input
    |> List.indexed
    |> List.fold
        (fun state (i, row) ->
            row
            |> List.indexed
            |> List.fold
                (fun innerState (j, char) ->
                    if char = "#" then
                        Set.add (i, j, 0) innerState
                    else
                        innerState)
                state)
        Set.empty

let deltas =
    [ 0; 1; -1 ]
    |> List.allPairs [ 0; 1; -1 ]
    |> List.allPairs [ 0; 1; -1 ]
    |> List.map (fun (a, (b, c)) -> (a, b, c))
    |> List.except [ (0, 0, 0) ]

let neighbours tupl =
    let a', b', c' = tupl

    deltas
    |> List.map (fun (a, b, c) -> (a' + a, b' + b, c' + c))

let range xs =
    ((Set.minElement xs) - 1, (Set.maxElement xs) + 1)

let ranges xss =
    (xss |> Set.map (fun (a, _, _) -> a) |> range,
     xss |> Set.map (fun (_, b, _) -> b) |> range,
     xss |> Set.map (fun (_, _, c) -> c) |> range)

let points xss =
    let xs, ys, zs = ranges xss

    seq {
        for x in (fst xs) .. (snd xs) do
            for y in (fst ys) .. (snd ys) do
                for z in (fst zs) .. (snd zs) -> (x, y, z)
    }
    |> List.ofSeq

let rec step i currentCoords pointsFun neighboursFun =
    if i = 6 then
        currentCoords
    else
        let ps = pointsFun currentCoords

        let newCoords =
            ps
            |> List.fold
                (fun state cur ->
                    let friends =
                        cur
                        |> neighboursFun
                        |> set
                        |> Set.intersect currentCoords
                        |> Set.count

                    let currentIsOn = Set.contains cur currentCoords

                    match currentIsOn with
                    | false ->
                        if friends = 3 then
                            Set.add cur state
                        else
                            state
                    | true ->
                        if friends = 2 || friends = 3 then
                            Set.add cur state
                        else
                            state)
                Set.empty

        step (i + 1) newCoords pointsFun neighboursFun

step 0 initialCoords points neighbours
|> Set.count
|> printfn "%A"

let deltas4 =
    [ 0; 1; -1 ]
    |> List.allPairs [ 0; 1; -1 ]
    |> List.allPairs [ 0; 1; -1 ]
    |> List.map (fun (a, (b, c)) -> (a, b, c))
    |> List.allPairs [ 0; 1; -1 ]
    |> List.map (fun (a, (b, c, d)) -> (a, b, c, d))
    |> List.except [ (0, 0, 0, 0) ]

let ranges4 xss =
    (xss |> Set.map (fun (a, _, _, _) -> a) |> range,
     xss |> Set.map (fun (_, b, _, _) -> b) |> range,
     xss |> Set.map (fun (_, _, c, _) -> c) |> range,
     xss |> Set.map (fun (_, _, _, d) -> d) |> range)

let points4 xss =
    let xs, ys, zs, ws = ranges4 xss

    seq {
        for x in (fst xs) .. (snd xs) do
            for y in (fst ys) .. (snd ys) do
                for z in (fst zs) .. (snd zs) do
                    for w in (fst ws) .. (snd zs) -> (x, y, z, w)
    }
    |> List.ofSeq

let neighbours4 tupl =
    let a', b', c', d' = tupl

    deltas4
    |> List.map (fun (a, b, c, d) -> (a' + a, b' + b, c' + c, d' + d))

let initialCoords4 =
    initialCoords
    |> Set.map
        (fun x ->
            let (a, b, c) = x
            a, b, c, 0)

step 0 initialCoords4 points4 neighbours4
|> Set.count
|> printfn "%A"
