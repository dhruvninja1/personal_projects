import { useUsernameState } from "../context/UsernameContext";
import Overlay from "./Overlay";
function Pause(){
    const { usernameValue } = useUsernameState();
    console.log(usernameValue);
    return(
        <div id='test'>
            {usernameValue!= 'Anonymous' ? (null) : (<Overlay zIndex={998}></Overlay>)}
        </div>
    )
}

export default Pause;

