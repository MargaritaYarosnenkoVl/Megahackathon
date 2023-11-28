import { useState } from 'react';
import { useSelector } from 'react-redux';
import Content from '../../content/Content';
import Header from '../../header/Header';
import Layout from '../../layout/Layout';
import LeftPanel from '../../left-panel/LeftPanel';
import NewsInOtherPage from '../../news-in-other-page/NewsInOtherPage';
import TitleList from '../../title-list/TitleList';
import BlockSearch from '../../ui/block-search/BlockSearch';
import NavigateBar from '../../ui/navigate-bar/NavigateBar';
import styles from './Favorite.module.scss';

const Favorite = () => {
	const [focusNews, setFocusNews] = useState();
	const user = useSelector(state => state.users[0]); //TODO: КАК Я БУДУ НАХОДИТЬ ЮЗЕРА: СДЕЛАТЬ КАСТОМНЫЙ ХУК КОТОРЫЙ ПРИ АВТОРИЗАЦИИ СДЕЛАЕТ ЗАПРОС О ЮЗЕРЕ И ЗАПИШЕТ ИНФУ В РЕДАКС, А ОТ ТУДА Я ВОЗЬМУ ID ИЛИ ЕСЛИ ОН 1, ТО НИЧЕГО МЕНЯТЬ НЕ БУДУ

	return (
		<Layout>
			<Header />
			<Content>
				<LeftPanel />
				<div className={styles.main}>
					<NavigateBar location='favorite' />
					<BlockSearch
						doubleBlock='yes'
						focusNews={focusNews}
						setFocusNews={setFocusNews}
					/>
					<TitleList />
					<div className={styles.block__resultFavorite}>
						{user.news.favoritesNews.map(news => {
							return (
								<NewsInOtherPage
									key={news.id}
									news={news}
									setFocusNews={setFocusNews}
									focusNews={focusNews}
								/>
							);
						})}
					</div>
				</div>
			</Content>
		</Layout>
	);
};

export default Favorite;
