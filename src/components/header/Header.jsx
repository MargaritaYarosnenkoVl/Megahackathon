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
					<InputSearch filter='yes' />
					<img src='../../images/icons/logoHeader.svg' alt='logo' />
				</div>
			)}
		</>
	);
};

export default Header;
