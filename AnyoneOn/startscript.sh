
cd $HOME
cd personal_projects
source personal/bin/activate

cd AnyoneOn/v$1/host

gnome-terminal -- bash -c "python serverManagement.py; exec bash"
gnome-terminal -- bash -c "python statusServerProxy.py; exec bash"
gnome-terminal -- bash -c "python statusServer.py 18080; exec bash"
gnome-terminal -- bash -c "python statusServer.py 18081; exec bash"
wait