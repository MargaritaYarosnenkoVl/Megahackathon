import Header from '../../header/Header';
import Layout from '../../layout/Layout';
import LeftPanel from '../../left-panel/LeftPanel';
import Content from '../../content/Content';
import styles from './UserList.module.scss';
import { Link } from 'react-router-dom';
import { useUsers } from '../../../hooks/useUsers';
import User from './User';
import Pagination from './Pagination';
import { useState } from 'react';
import Button from '../../ui/button/Button';


const UserList = () => {
    const {infoUsers, get_users } = useUsers();
	
    const [currentPage, setCurrentPage] = useState(1);
    const [usersPerPage] = useState(10);

    const lastUserIndex = currentPage * usersPerPage;
    const firstUserIndex = lastUserIndex - usersPerPage;
    const currentUsers = infoUsers.slice(firstUserIndex, lastUserIndex);
   
    const paginate = pageNumber => setCurrentPage(pageNumber);
    
    const nextPage = () => setCurrentPage( prev => prev + 1);
    const prevPage = () => setCurrentPage( prev => prev - 1);


    return (
        <Layout justifyContent='space-between'>
            <Header/>
            <Content>
				<LeftPanel />
                <div className={styles.wrapper}>
                    <div className={styles.block__users}>
                        <div className={styles.block__navigation}>
                            <Link to={'/home'}>Главная</Link>
                            <p>/</p>
                            <Link to={'/home/personalArea'}>Личный кабинет</Link>
                            <p>/</p>
                            <p>Пользователи</p>
                        </div>
                        <div className={styles.block__table}>
                            <table>
                                <thead>
                                    <tr> 
                                        <th>Пользователь</th>
                                        <th>ФИО</th>
                                        <th>E-mail</th>
                                        <th>Дата регистрации</th>
                                        <th></th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {currentUsers.map((user) => <User key={user.id} user={user} />)}
                                </tbody>
                            </table> 
                        </div>
                        <div className={styles.block__content}>
                            <Button saveInfo='add_user'>
                               + Добавить нового
                            </Button>
                        </div>
                        <Pagination 
                            usersPerPage={usersPerPage} 
                            totalUsers={infoUsers.length} 
                            paginate={paginate}
                            nextPage={nextPage}
                            prevPage={prevPage}
                            currentPage={currentPage}
                        />
                    </div>
                </div>
			</Content>
        </Layout>
	);
};

export default UserList;
