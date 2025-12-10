import { useServerState } from "../context/ServerContext";
import { useState } from "react";

function PortReveal(){
    const { serverValue } = useServerState();
    const [revealed, setRevealed] = useState(false);
    const handleClick = ()=> {
        setRevealed(!revealed);
        console.log(revealed);
    }

    return(
        <button onClick={handleClick}>{revealed ? (serverValue) : ('*****')}</button>
    )
}

export default PortReveal;