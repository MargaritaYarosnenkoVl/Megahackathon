// import { Link, useNavigate } from "react-router-dom";
import { useState } from 'react';
import styles from './User.module.scss'


function User(props) {
    const date = new Date(props.user.registred_at)

    return(
        <>
            <tr key={props.user.id} >
                <td>{props.user.username}</td>
                <td>{props.user.full_name}</td>
                <td>{props.user.email}</td>
                <td>{new Intl.DateTimeFormat().format(date)}</td>
                <td className={styles.header__buttons}> 
                    <button>
                        <img
                            src='../../../../public/images/icons/checkbox_users.svg'
                            alt='image'
                        />
					</button>
                    <button>
                        <img
                            src='../../../../public/images/icons/change_users.svg'
                            alt='image'
                        />
					</button>
                    <button>
                        <img
                            src='../../../../public/images/icons/delete_users.svg'
                            alt='image'
                        />
					</button>
                </td>
            </tr>
        </>
    );
}

export default User;