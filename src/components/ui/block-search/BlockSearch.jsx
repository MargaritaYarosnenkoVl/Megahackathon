import { useDispatch } from 'react-redux';
import { actions } from '../../../store/users/Users.slice';
import Button from '../button/Button';
import InputSearch from '../input-search/InputSearch';
import styles from './BlockSearch.module.scss';

const BlockSearch = ({ doubleBlock, focusNews, setFocusNews }) => {
	const dispatch = useDispatch();

	return (
		<>
			{doubleBlock !== 'yes' ? (
				<div className={styles.block__search}>
					<InputSearch />
					<Button saveInfo='search'>Поиск</Button>
				</div>
			) : (
				<>
					<div className={styles.block__search_yes}>
						<div className={styles.block__one}>
							<InputSearch />
							<Button saveInfo='search'>Поиск</Button>
						</div>

						<div className={styles.add_and_delete}>
							<p>1 выделенный объект</p>
							<div className={styles.block__button}>
								<button>
									Добавить
									<img src='../images/icons/plus_white.svg' alt='img' />
								</button>
								<button
									onClick={() => {
										dispatch(actions.deleteNewsFromHistory(focusNews));
										setFocusNews(null);
									}}
								>
									Удалить
									<img src='../images/icons/basketDelete.svg' alt='img' />
								</button>
							</div>
						</div>
					</div>
				</>
			)}
		</>
	);
};

export default BlockSearch;
