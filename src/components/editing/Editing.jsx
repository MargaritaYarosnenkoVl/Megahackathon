import styles from './Editing.module.scss';

const Editing = ({
	isViewEditNews,
	setIsViewEditNews,
	editingNews,
	setEditingNews,
}) => {
	return (
		<div className={styles.editing}>
			{isViewEditNews && (
				<>
					<div className={styles.header__edit}>
						<a href='#'>К источнику</a>
						<div className={styles.header__buttons}>
							<button>
								<img src='./images/icons/vector_active_white.svg' alt='image' />
							</button>
							<button>
								<img src='./images/icons/marker_active_white.svg' alt='image' />
							</button>
							<button>
								<img
									src='./images/icons/favorite_active_white.svg'
									alt='image'
								/>
							</button>
							<button>
								<img
									src='./images/icons/foulder_active_white.svg'
									alt='image'
								/>
							</button>
							<button>
								<img
									src='./images/icons/focus_edit_active_white.svg'
									alt='image'
								/>
							</button>
							<button>
								<img
									src='./images/icons/exit_edit_active_white.svg'
									alt='image'
								/>
							</button>
						</div>
					</div>
					<h2>{editingNews.title}</h2>
					<p>{editingNews.preview}</p>
					<p>{editingNews.date}</p>
					<p>{editingNews.description}</p>
					<p>{editingNews.source}</p>
				</>
			)}
		</div>
	);
};

export default Editing;
