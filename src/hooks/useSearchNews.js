import axios from 'axios';
import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { useSelector } from 'react-redux';
import { useResultNews } from './useResultNews';

const useSearchNews = () => {
	const user = useSelector(state => state.users[0]);

	const { request, setRequest } = useResultNews();
	const [formData, setFormData] = useState();

	const arrayAdres = [
		'naked-science.ru',
		'portal-kultura.ru',
		'3dnews.ru',
		'snob.ru',
		'windozo.ru',
		'fontanka.ru',
		'knife.media',
		'nplus1.ru',
		'sdelanounas.ru',
		'forbes.ru',
		'cnews.ru',
		'dimonvideo.ru',
		'techno-news.net',
	];

	const {
		register,
		handleSubmit,
		formState: { errors },
	} = useForm({
		mode: 'onChange',
	});

	const searchCheck = value => {
		for (let cite in value) {
			if (value[cite]) return cite;
		}
	};

	const adresCheck = (cite, arrAdres) => {
		const lengthCite = cite.length;

		const result = arrAdres.find(link =>
			link.substring(0, lengthCite) === cite ? link : ''
		);
		return result;
	};

	const onSubmit = async data => {
		setFormData(data);
		console.log(formData);
		try {
			const response = await axios.post(
				'https://212.20.45.230:8004/schedule/spider',
				{
					origin: { parsed_from: adresCheck(searchCheck(data), arrayAdres) },
					username: {
						name: user.name,
					},
				}
			);
			setRequest({
				origin: { parsed_from: adresCheck(searchCheck(data), arrayAdres) },
				username: {
					name: user.name,
				},
			});
			console.log(response);
		} catch (error) {
			console.log(error);
		}
	};

	const result = async () => {
		try {
			const response = await axios.post(
				'https://212.20.45.230:8004/get/temp/filter',
				request
			);

			console.log(response);
		} catch (error) {
			console.log(error);
		}
	};

	return {
		searchCheck,
		adresCheck,
		register,
		handleSubmit,
		errors,
		onSubmit,
		result,
		user,
		request,
	};
};

export default useSearchNews;
