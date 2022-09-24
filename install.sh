echo -----------------------------------
apt install ocaml
rm hachage
ocamlopt hachage.ml -o hachage
rm hachage.cmi
rm hachage.cmx
rm hachage.o
pip3 install pickle-mixin
pip3 install flask
pip3 install Flask-Session
echo ------ Installation terminée ------

