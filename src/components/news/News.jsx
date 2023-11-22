import styles from './News.module.scss';

const News = ({
	news,
	setEditingNews,
	setIsViewEditNews,
	isViewEditNews,
	editingNews,
}) => {
	return (
		<div
			className={styles.news}
			style={
				isViewEditNews && editingNews.id === news.id
					? { backgroundColor: '#d0d9e2' }
					: {}
			}
		>
			<div className={styles.news__blockOne}>
				<p className={styles.news__id}>{news.id}</p>
				<h2 className={styles.news__title}>{news.title}</h2>
			</div>
			<p className={styles.news__preview}>{news.preview}</p>
			<div className={styles.news__blockTwo}>
				<div className={styles.news__block_date}>
					<p className={styles.news__date}>{news.date}</p>
					<p className={styles.news__source}>{news.source}</p>
				</div>
				<div className={styles.news__block_buttons}>
					<button>
						<img src='./images/icons/vector.svg' alt='image' />
					</button>
					<button>
						<img src='./images/icons/marker.svg' alt='image' />
					</button>
					<button>
						<img src='./images/icons/favorite.svg' alt='image' />
					</button>
					<button>
						<img src='./images/icons/foulder.svg' alt='image' />
					</button>
					<button
						onClick={() => {
							setEditingNews({
								id: news.id,
								title: news.title,
								preview: news.preview,
								date: news.date,
								source: news.source,
								description: news.description,
							});

							setIsViewEditNews(!isViewEditNews);
						}}
					>
						{
							<img
								src={
									isViewEditNews && editingNews.id === news.id
										? './images/icons/focus_edit_active_blue.svg'
										: './images/icons/focus_edit.svg'
								}
								alt='image'
							/>
						}
					</button>
					<button>
						<img src='./images/icons/exit_edit.svg' alt='image' />
					</button>
				</div>
			</div>
		</div>
	);
};

export default News;
