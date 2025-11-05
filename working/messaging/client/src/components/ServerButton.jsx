import { useServerState } from '../context/ServerContext';
import { emitUsername } from './socket';
import { useUsernameState } from '../context/UsernameContext';

function ServerButton({ key, port, name }){
    const { serverValue, updateServerValue } = useServerState();
    const {usernameValue} = useUsernameState();
    const handleClick = () => {
        console.log('Switching to server:', port);
        updateServerValue(port);
        console.log('Server selected:', port);
        emitUsername(usernameValue);

    }
    return(
        <button style={{border: '1px solid gray', borderRadius: 'md', padding: '2px'}} onClick={handleClick}>{name}</button>
    )
}

export default ServerButton;