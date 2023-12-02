import { useState } from 'react';
import styles from './User.module.scss';
import { $axios } from '../../../api';
import Modal from '../../ui/modal/Modal';
import Cookies from 'js-cookie';
import { TOKEN } from '../../../app.constants';
import { useUsers } from '../../../hooks/useUsers';
import ChangeUser from './change-user-info/ChangeUser';


function User(props) {
    const {get_users} = useUsers();
    const token = Cookies.get(TOKEN);
    const date = new Date(props.user.registred_at);
    const [deleteModalActive, setDeleteModalActive] = useState(false);
    const [changeModalActive, setChangeModalActive] = useState(false);
    

    const delete_user = async () => {
        const requestOptions = {
			headers: { 
                "Content-Type": "application/x-www-form-urlencoded",
                'Authorization': 'Bearer ' + token,
			},
		};
		try {
			const responce = await $axios.delete(`https://212.20.45.230:8004/users/${props.user.id}`, requestOptions);
			console.log(responce.data);
            get_users();
		} catch (error) {
			console.log(error);
		}
	};


    const deleteHandler = () => {
        delete_user();
        setDeleteModalActive(false);
        console.log(`Пользователь ${props.user.username} удален.`);
    };


    return(
        <>
            <tr key={props.user.id} >
                <td>{props.user.username}</td>
                <td>{props.user.full_name}</td>
                <td>{props.user.email}</td>
                <td>{new Intl.DateTimeFormat().format(date)}</td>
                <td className={styles.header__buttons}> 
                    {/* <button>
                        <img
                            src='../../../../public/images/icons/checkbox_users.svg'
                            alt='image'
                        />
					</button> */}
                    <button onClick={() => {setChangeModalActive(true)}}>
                        <img
                            src='../../../../public/images/icons/change_users.svg'
                            alt='image'
                        />
					</button>
                    <button onClick={() => {setDeleteModalActive(true)}}>
                        <img
                            src='../../../../public/images/icons/delete_users.svg'
                            alt='image'
                        />
					</button>
                </td>
            </tr>
            <Modal active={deleteModalActive} setActive={setDeleteModalActive}> 
                <div className={styles.modal__text}>
                    <p>Удалить пользователя {props.user.username}?</p>
                </div>
                <div className={styles.modal__buttons}>
                    <button onClick={deleteHandler}>
                            Да
                    </button>
                    <button onClick={() => {setDeleteModalActive(false)}}>
                            Нет
                    </button>
                </div>
            </Modal>
            <Modal view='change' active={changeModalActive} setActive={setChangeModalActive}> 
                <ChangeUser user={props.user} setChangeModalActive={setChangeModalActive}/>
            </Modal>
        </>
    );
}

export default User;