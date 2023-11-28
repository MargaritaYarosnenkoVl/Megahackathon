import Content from '../../content/Content';
import Header from '../../header/Header';
import InsideInfo from '../../inside-info/InsideInfo';
import Layout from '../../layout/Layout';
import LeftPanel from '../../left-panel/LeftPanel';

const PersonalArea = () => {
	return (
		<Layout justifyContent='space-between'>
			<Header />
			<Content>
				<LeftPanel />
				<InsideInfo />
			</Content>
		</Layout>
	);
};

export default PersonalArea;
