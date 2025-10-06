import { useServerState } from '../context/ServerContext';

function ServerButton({ key, port }){
    const { serverValue, updateServerValue } = useServerState();
    const handleClick = () => {
        console.log('Switching to server:', port);
        updateServerValue(port);
        console.log('Server selected:', port);
    }
    return(
        <button onClick={handleClick}>Test</button>
    )
}

export default ServerButton;