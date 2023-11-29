import InputSearch from '../ui/input-search/InputSearch';
import styles from './Header.module.scss';

const Header = ({ search }) => {
	return (
		<>
			{search !== 'search' ? (
				<div className={styles.wrapper}>
					<img src='../../images/icons/logoHeader.svg' alt='logo' />
				</div>
			) : (
				<div className={styles.wrapper__search}>
					{/* <div className={styles.block__header_settings}>
						<div className={styles.block__search}>
							<img
								className={styles.search__image}
								src='./images/icons/search.svg'
								alt='search'
							/>
							<input
								className={styles.search}
								type='text'
								placeholder='Поиск'
							/>
						</div>
						<button className={styles.button__filtr}>
							<img src='./images/icons/filtr.svg' alt='img' />
							Фильтры
						</button>
					</div> */}
					<InputSearch filter='yes' />
					<img src='../../images/icons/logoHeader.svg' alt='logo' />
				</div>
			)}
		</>
	);
};

export default Header;
