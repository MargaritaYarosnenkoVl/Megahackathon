import { useCheckToken } from '../../hooks/useCheckToken';
import styles from './Layout.module.scss';

const Layout = ({ children, bgImage, justifyContent }) => {
	useCheckToken();

	return (
		<div
			className={styles.wrapper}
			style={{
				backgroundImage: `url('${bgImage}')`,
				justifyContent: justifyContent,
			}}
		>
			{children}
		</div>
	);
};

export default Layout;
