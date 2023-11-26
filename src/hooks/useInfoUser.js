import { useState } from 'react';
import { useDispatch } from 'react-redux';
import { actions } from '../store/users/Users.slice';

export const useInfoUser = () => {
	const [name, setName] = useState('Иванов Иван Иванович');
	const [prof, setProf] = useState('Директор');
	const [mobile, setMobile] = useState('8-921-951-95-95');
	const [email, setEmail] = useState('tix@yandex.ru');
	const [profileImage, setProfileImage] = useState(null);

	const [isViewName, setIsViewName] = useState(false);
	const [isViewProf, setIsViewProf] = useState(false);
	const [isViewMobile, setIsViewMobile] = useState(false);
	const [isViewEmail, setIsViewEmail] = useState(false);

	const dispatch = useDispatch();

	const handleFileChange = event => {
		const file = event.target.files[0];

		if (file) {
			const imageUrl = URL.createObjectURL(file);
			setProfileImage(imageUrl);
			console.log(profileImage);
		}
	};

	const confirmImage = () => {
		console.log(profileImage);
		dispatch(actions.addURLImage(profileImage)); //TODO: Разобраться с добавлением ссылки
	};

	const deleteFileChange = () => {
		setProfileImage(null);
	};

	const repeatPassword = (main, two) => {
		return main === two;
	};

	// console.log({
	// 	name,
	// 	profession: prof,
	// 	number: mobile,
	// 	email,
	// 	password: repeatPassword() ? mainPassword : undefined,
	// });

	return {
		dispatch,
		name,
		setName,
		prof,
		setProf,
		mobile,
		setMobile,
		email,
		setEmail,
		profileImage,
		setProfileImage,
		isViewName,
		setIsViewName,
		isViewProf,
		setIsViewProf,
		isViewMobile,
		setIsViewMobile,
		isViewEmail,
		setIsViewEmail,
		handleFileChange,
		confirmImage,
		deleteFileChange,
		repeatPassword,
	};
};
