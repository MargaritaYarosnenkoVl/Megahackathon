import { useEffect, useState } from 'react';
import { useSelector } from 'react-redux';
import { useFilter } from '../../../hooks/useFilter';
import { useUser } from '../../../hooks/useUser';
import { useUsers } from '../../../hooks/useUsers';
import { FilterContext } from '../../../providers/FilterProvider';
import Content from '../../content/Content';
import Editing from '../../editing/Editing';
import Header from '../../header/Header';
import Layout from '../../layout/Layout';
import LeftPanel from '../../left-panel/LeftPanel';
import News from '../../news/News';
import WindowFilter from '../../window-filter/WindowFilter';
import styles from './Home.module.scss';
import { useResultNews } from '../../../hooks/useResultNews';

const Home = () => {
	const users = useSelector(state => state.users[0]);
	const { responseNews, setResponseNews } = useResultNews({});

	const [editingNews, setEditingNews] = useState();
	const [isViewEditNews, setIsViewEditNews] = useState(false);

	const { isViewFilter } = useFilter(FilterContext);
	const { infoUser, get_user } = useUser();
	const { infoUsers, get_users } = useUsers();

	useEffect(() => {
		console.log(editingNews);
		console.log(isViewEditNews);
		if (!infoUser) {
			get_user();
			console.log(infoUser);
		}
		if (!infoUsers) {
			get_users();
		}
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
						<p className={styles.allNews}>
							Всего {users.news.newNews.length} новости
						</p>
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
					{/* {responseNews.map(news => {
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
					})} */}
				</div>
				<Editing
					setEditingNews={setEditingNews}
					setIsViewEditNews={setIsViewEditNews}
					editingNews={editingNews}
					isViewEditNews={isViewEditNews}
				/>
			</Content>
			{isViewFilter && <WindowFilter />}
		</Layout>
	);
};

export default Home;
