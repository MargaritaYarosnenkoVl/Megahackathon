import styles from './Header.module.scss';

const Header = () => {
	return (
		<div className={styles.wrapper}>
			<img src='./images/icons/logoHeader.svg' alt='logo' />
		</div>
	);
};

export default Header;
