cd $HOME
cd personal_projects
source personal/bin/activate

cd AnyoneOn/v$1/host

gnome-terminal -- bash -c "python serverManagement.py; exec bash"
gnome-terminal -- bash -c "python statusServerProxy.py; exec bash"

items=$(jq -c '.[]' data/openServers.json)

for item in $items; do
    gnome-terminal -- bash -c "python statusServer.py $item; exec bash"
done

wait