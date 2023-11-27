import { useState } from 'react';
import useDescriptionLength from '../../hooks/useDescriptionLength';
import styles from './NewsInOtherPage.module.scss';

const NewsInOtherPage = ({ news, focusNews, setFocusNews }) => {
	const { truncateDescription } = useDescriptionLength();

	const [isCheckbox, setIsCheckbox] = useState(false);

	return (
		<div
			className={styles.wrapper_news}
			onClick={() => {
				setFocusNews(news.id);
				setIsCheckbox(!isCheckbox);
			}}
			style={
				isCheckbox && focusNews === news.id
					? { backgroundColor: '#f3f3f3' }
					: {}
			}
		>
			<div className={styles.block__one}>
				<img
					className={styles.image__arrow}
					src='../images/icons/arrow_bottom.svg'
					alt='img'
				/>
				<button onClick={() => setIsCheckbox(!isCheckbox)}>
					<img
						src={
							isCheckbox
								? '../images/icons/checkbox_on.svg'
								: '../images/icons/checkbox_off.svg'
						}
						alt='img'
					/>
				</button>
				<p>{news.source}</p>
			</div>

			<h2>{news.title}</h2>
			<div className={styles.block__two}>
				<button>
					<img src='../images/icons/favorite.svg' alt='img' />
				</button>
				<button>
					<img src='../images/icons/edit_gray.svg' alt='img' />
				</button>
				<button>
					<img src='../images/icons/basketDelete_gray.svg' alt='img' />
				</button>
				<button>
					<img src='../images/icons/more.svg' alt='img' />
				</button>
			</div>

			<p>{news.teg ? truncateDescription(news.teg, 50) : ''}</p>
		</div>
	);
};

export default NewsInOtherPage;
