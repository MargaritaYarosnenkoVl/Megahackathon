import axios from 'axios';
import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { useSelector } from 'react-redux';
import { useResultNews } from './useResultNews';
import { useUser } from './useUser';

const useSearchNews = () => {
	const user = useSelector(state => state.users[0]);
	const {infoUser} = useUser();

	const { request, setRequest, responseNews, setResponseNews } = useResultNews({});
	const [formData, setFormData] = useState();
	const [parseToken, setParseToken] = useState();

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
						name: infoUser.username,
					},
				}
			);
			setRequest({
				username: {
					name: infoUser.username,
				},
				origin: { parsed_from: adresCheck(searchCheck(data), arrayAdres) },
			});
			console.log(response);
			setParseToken(response.data);
		} catch (error) {
			console.log(error);
		}
	};

	const result = async () => {
		try {
			const response = await axios.post(
				'https://212.20.45.230:8004/temp/filter',
				request
			);
			console.log(response.data);
			const data = response.data;
			setResponseNews(data);
		} catch (error) {
			console.log(error);
		}
	};


	const stop_parse = async () => {
		try {
			const response = await axios.post(
				'https://212.20.45.230:8004/schedule/spider/stop',
				{
					job_id: {parseToken}
				}
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
		stop_parse,
		responseNews,
	};
};

export default useSearchNews;
