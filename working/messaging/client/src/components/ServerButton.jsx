import { useServerState } from '../context/ServerContext';

function ServerButton({ key, port, name }){
    const { serverValue, updateServerValue } = useServerState();
    const handleClick = () => {
        console.log('Switching to server:', port);
        updateServerValue(port);
        console.log('Server selected:', port);
    }
    return(
        <button style={{border: '1px solid gray', borderRadius: 'md', padding: '2px'}} onClick={handleClick}>{name}</button>
    )
}

export default ServerButton;