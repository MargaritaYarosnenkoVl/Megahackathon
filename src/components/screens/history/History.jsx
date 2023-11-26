import { useState } from 'react';
import { useSelector } from 'react-redux';
import Content from '../../content/Content';
import Header from '../../header/Header';
import Layout from '../../layout/Layout';
import LeftPanel from '../../left-panel/LeftPanel';
import BlockSearch from '../../ui/block-search/BlockSearch';
import NavigateBar from '../../ui/navigate-bar/NavigateBar';
import styles from './History.module.scss';

const History = () => {
	const user = useSelector(store => store.users[0]);
	const [isCheckbox, setIsCheckbox] = useState();

	return (
		<Layout>
			<Header />
			<Content>
				<LeftPanel />
				<div className={styles.main}>
					<NavigateBar location='history' />
					<BlockSearch doubleBlock='yes' />
					<div className={styles.block__resultHistory}>
						{user.news.viewHistoryNews.map(news => {
							return (
								<div>
									<img src='../images/icons/arrow_bottom.svg' alt='img' />
									{isCheckbox ? (
										<img src='../images/icons/checkbox_on.svg' alt='img' />
									) : (
										<img src='../images/icons/checkbox_off.svg' alt='img' />
									)}
									<p>{news.source}</p>
									<h2>{news.title}</h2>
									<button>
										<img src='../images/icons/favorite.svg' alt='img' />
									</button>
									<button>
										<img src='../images/icons/favorite.svg' alt='img' />
									</button>
									<button>
										<img src='../images/icons/favorite.svg' alt='img' />
									</button>
									<button>
										<img src='../images/icons/more.svg' alt='img' />
									</button>
									<p>{news?.teg}</p>
								</div>
							);
						})}
					</div>
				</div>
			</Content>
		</Layout>
	);
};

export default History;
