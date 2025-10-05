function Overlay(){
    return(
        <div className="overlay" id="overlay" style={{ position: 'fixed', 
                                                           top: 0, 
                                                           left: 0, 
                                                           width: '100%', 
                                                           height: '100%', 
                                                           backgroundColor: 'rgba(0, 0, 0, 0.5)', 
                                                           zIndex: 999 }}>
          </div>
    )
}

export default Overlay;