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
import styles from './LaterRead.module.scss';

const LaterRead = () => {
	const [focusNews, setFocusNews] = useState();
	const user = useSelector(state => state.users[0]);

	return (
		<Layout>
			<Header />
			<Content>
				<LeftPanel />
				<div className={styles.main}>
					<NavigateBar location='later' />
					<BlockSearch
						doubleBlock='yes'
						focusNews={focusNews}
						setFocusNews={setFocusNews}
					/>
					<TitleList />
					<div className={styles.block__resultLater}>
						{user.news.viewLaterNews.map(news => {
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

export default LaterRead;
