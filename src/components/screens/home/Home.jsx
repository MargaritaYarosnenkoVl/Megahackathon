import { useEffect, useState } from 'react';
import { useSelector } from 'react-redux';
import Content from '../../content/Content';
import Editing from '../../editing/Editing';
import Header from '../../header/Header';
import Layout from '../../layout/Layout';
import LeftPanel from '../../left-panel/LeftPanel';
import News from '../../news/News';
import styles from './Home.module.scss';
import { useUser } from '../../../hooks/useUser';
import { useUsers } from '../../../hooks/useUsers';


const Home = () => {
	const users = useSelector(state => state.users[0]);

	const [editingNews, setEditingNews] = useState();
	const [isViewEditNews, setIsViewEditNews] = useState(false);
	const {infoUser, get_user} = useUser();
	const {infoUsers, get_users} = useUsers();

	useEffect(() => {
		console.log(editingNews);
		console.log(isViewEditNews);
		if(!infoUser){
			get_user();
			console.log(infoUser);
		};
		if(!infoUsers){
			get_users();
		};
	}, [editingNews, infoUser]);

	return (
		<Layout justifyContent='space-between'>
			<Header search='search' />
			<Content>
				<LeftPanel />
				<div className={styles.block__news}>
					<div className={styles.block__sorting}>
						<button className={styles.button__sorting}>
							<img src='./images/icons/arrow_down_up.svg' alt='img' />
							Сортировка
						</button>
						<p className={styles.allNews}>Всего {users.news.length} новости</p>
					</div>

					{users.news.newNews.map(news => {
						return (
							<News
								key={news.id}
								setEditingNews={setEditingNews}
								setIsViewEditNews={setIsViewEditNews}
								editingNews={editingNews}
								isViewEditNews={isViewEditNews}
								news={news}
							/>
						);
					})}
				</div>
				<Editing
					setEditingNews={setEditingNews}
					setIsViewEditNews={setIsViewEditNews}
					editingNews={editingNews}
					isViewEditNews={isViewEditNews}
				/>
			</Content>
		</Layout>
	);
};

export default Home;
