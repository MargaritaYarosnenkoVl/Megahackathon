import styles from './InputSearch.module.scss';

const InputSearch = ({ filter }) => {
	return (
		<div className={styles.block__header_settings}>
			<div className={styles.block__search}>
				<img
					className={styles.search__image}
					src='../images/icons/search.svg'
					alt='search'
				/>
				<input className={styles.search} type='text' placeholder='Поиск' />
			</div>

			{filter === 'yes' && (
				<button className={styles.button__filtr}>
					<img src='../images/icons/filtr.svg' alt='img' />
					Фильтры
				</button>
			)}
		</div>
	);
};

export default InputSearch;
