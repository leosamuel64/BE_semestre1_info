let rec convert l=
  match l with
  | []-> []
  | t::q -> (String.make 1 t) ::(convert q)
  ;;

let explode s =
  let rec expl i l =
    if i < 0 then l else
    expl (i - 1) (s.[i] :: l) in
  expl (String.length s - 1) [];;

let rec reverse chaine=
  match chaine with
  | [] -> ""
  | t::q -> reverse q ^ t 
;;


let hash mdp=
  Hashtbl.hash mdp;;

print_int (hash Sys.argv.(1));;