import { useState } from 'react';
import Button from '../ui/button/Button';
import styles from './Editing.module.scss';

const Editing = ({
	isViewEditNews,
	setIsViewEditNews,
	editingNews,
	setEditingNews,
}) => {
	const [isEditTitle, setIsEditTitle] = useState(false);
	const [isEditDate, setIsEditDate] = useState(false);
	const [isEditSource, setIsEditSource] = useState(false);

	return (
		<div className={styles.editing}>
			{isViewEditNews && (
				<>
					<div className={styles.header__edit}>
						<a href='#'>К источнику</a>
						<div className={styles.header__buttons}>
							<button>
								<img src='./images/icons/edit.svg' alt='image' />
							</button>
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
					<form>
						{isEditTitle ? (
							<input
								className={styles.title}
								defaultValue={editingNews.title}
							/>
						) : (
							<h2 className={styles.title}>{editingNews.title}</h2>
						)}
						<div className={styles.block__date}>
							{isEditDate ? (
								<input
									className={styles.date}
									type='text'
									defaultValue={editingNews.date}
								/>
							) : (
								<p className={styles.date}>{editingNews.date}</p>
							)}
							{isEditSource ? (
								<input
									className={styles.source}
									type='text'
									defaultValue={editingNews.source}
								/>
							) : (
								<p className={styles.source}>{editingNews.source}</p>
							)}
						</div>
						<textarea
							className={styles.description}
							defaultValue={editingNews.description}
						></textarea>
						<input
							className={styles.teg}
							type='text'
							placeholder='ДОБАВИТЬ ТЕГИ'
						/>
						<textarea
							className={styles.comments}
							placeholder='Комментарии'
						></textarea>
						<div className={styles.block__buttons}>
							<Button>отмена</Button>
							<Button>Сохранить</Button>
						</div>
					</form>
				</>
			)}
		</div>
	);
};

export default Editing;
