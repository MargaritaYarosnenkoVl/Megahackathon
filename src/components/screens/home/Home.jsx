import { useEffect, useState } from 'react';
import { useSelector } from 'react-redux';
import { $axios } from '../../../api';
import Content from '../../content/Content';
import Editing from '../../editing/Editing';
import Header from '../../header/Header';
import Layout from '../../layout/Layout';
import LeftPanel from '../../left-panel/LeftPanel';
import News from '../../news/News';
import styles from './Home.module.scss';

const Home = () => {
	const test = async () => {
		try {
			const responce = await $axios.get('https://212.20.45.230:8004/users/me');
			console.log(await responce);
		} catch (error) {
			console.log(error);
		}
	};

	const users = useSelector(state => state.users[0]);

	const [editingNews, setEditingNews] = useState();
	const [isViewEditNews, setIsViewEditNews] = useState(false);

	useEffect(() => {
		console.log(editingNews);
		console.log(isViewEditNews);
	}, [editingNews]);

	return (
		<Layout justifyContent='space-between'>
			<Header />
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

					{users.news.map(news => {
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
			<button onClick={test}>test</button>
		</Layout>
	);
};

export default Home;
