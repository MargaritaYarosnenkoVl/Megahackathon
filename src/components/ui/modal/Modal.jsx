import React, { Children } from "react";
import styles from './Modal.module.scss';


const Modal = ({active, setActive, children, view}) => {
    return (
        <>
            {view === 'change' ? (
                <div className={ active ? styles.active : styles.modal} onClick={() => {setActive(false)}}>
                    <div className={ active ? styles.modal__content__active__change : styles.modal__content } onClick={e => e.stopPropagation()}>
                        {children}
                    </div>
                </div>
            ) : (
                <div className={ active ? styles.active : styles.modal} onClick={() => {setActive(false)}}>
                    <div className={ active ? styles.modal__content__active : styles.modal__content } onClick={e => e.stopPropagation()}>
                        {children}
                    </div>
                </div>
            )}  
        </>
       
    );
};

export default Modal ;
