import { useUser } from '../../../hooks/useUser';
import Content from '../../content/Content';
import Header from '../../header/Header';
import InsideInfo from '../../inside-info/InsideInfo';
import InsideInfoAdmin from '../../inside-info/InsideInfoAdmin';
import Layout from '../../layout/Layout';
import LeftPanel from '../../left-panel/LeftPanel';

const PersonalArea = () => {
	const {infoUser} = useUser();

	return (
		<Layout justifyContent='space-between'>
			<Header />
			<Content>
				<LeftPanel />
				{infoUser.is_superuser? (
					<InsideInfoAdmin/>
				):(
					<InsideInfo />
				)}
			</Content>
		</Layout>
	);
};

export default PersonalArea;
