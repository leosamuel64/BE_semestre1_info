let hash mdp=
  Hashtbl.hash mdp;;

print_int (hash Sys.argv.(1));;