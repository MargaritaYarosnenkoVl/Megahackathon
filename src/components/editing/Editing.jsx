import { useState } from 'react';
import { useDispatch } from 'react-redux';
import { useEditNews } from '../../hooks/useEditNews';
import { actions } from '../../store/users/Users.slice';
import Button from '../ui/button/Button';
import styles from './Editing.module.scss';

const Editing = ({ isViewEditNews, editingNews }) => {
	const [isEditNews, setIsEditNews] = useState(false);
	const { register, handleSubmit, onSubmit, getValues } = useEditNews();

	const dispatch = useDispatch();

	return (
		<div className={styles.editing}>
			{isViewEditNews && (
				<>
					<div className={styles.header__edit}>
						<a href='#'>К источнику</a>
						<div className={styles.header__buttons}>
							<button onClick={() => setIsEditNews(!isEditNews)}>
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
					<form onSubmit={handleSubmit(onSubmit)}>
						{isEditNews ? (
							<input
								{...register('title')}
								className={styles.title}
								defaultValue={editingNews.title}
							/>
						) : (
							<h2 className={styles.title}>{editingNews.title}</h2>
						)}
						<div className={styles.block__date}>
							{isEditNews ? (
								<input
									{...register('date')}
									className={styles.date}
									type='text'
									defaultValue={editingNews.date}
								/>
							) : (
								<p className={styles.date}>{editingNews.date}</p>
							)}
							{isEditNews ? (
								<input
									{...register('source')}
									className={styles.source}
									type='text'
									defaultValue={editingNews.source}
								/>
							) : (
								<p className={styles.source}>{editingNews.source}</p>
							)}
						</div>
						{isEditNews ? (
							<textarea
								{...register('description')}
								className={styles.description}
								defaultValue={editingNews.description}
							></textarea>
						) : (
							<p className={styles.description}>{editingNews.description}</p>
						)}
						{isEditNews ? (
							<input
								{...register('teg')}
								className={styles.teg}
								type='text'
								placeholder='ДОБАВИТЬ ТЕГИ'
							/>
						) : (
							<p className={styles.teg}>ДОБАВИТЬ ТЕГИ</p>
						)}
						{isEditNews ? (
							<textarea
								{...register('comments')}
								className={styles.comments}
								placeholder='Комментарии'
							></textarea>
						) : (
							<p className={styles.comments}>Комментарии</p>
						)}

						<div className={styles.block__buttons}>
							<Button>отмена</Button>
							{/* <Button>Сохранить</Button> */}
							<button
								onClick={() =>
									dispatch(
										actions.addEditingNews({
											id: editingNews.id,
											title: getValues('title'),
											description: getValues('description'),
											date: getValues('date'),
											source: getValues('source'),
											teg: getValues('teg'),
											comments: getValues('comments'),
										})
									)
								}
							>
								Сохранить
							</button>
						</div>
					</form>
				</>
			)}
		</div>
	);
};

export default Editing;
