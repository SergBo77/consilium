import { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
   const [query, setQuery] = useState(''); /** поисковый запрос */
   const [response, setResponse] = useState(''); /** ответ с сервера */

   /** функция-обработчик поискового поля */
   const handleIputChange = ({ target }) => setQuery(target.value);

   /** функция отправки поискового запроса */
   const handleFormSubmit = async (e) => {
      /** предотвращаем перезагрузку страницы */
      e.preventDefault();

      /** конфигурация запроса */
      const config = {
         headers: {
            'Content-Type': 'application/json',
         },
      };

      /** делаем запрос на сервер */
      try {
         const { data } = await axios.post(import.meta.env.VITE_REQUEST_URL, query, config);
         setResponse(data);
      } catch (error) {
         console.log(error);
      }
   };

   return (
      <section className='container'>
         <header className='container_header'>
            <div className='container_logo'>
               <img src='/imgs/logo.png' alt='лого' className='container_header_img' />
            </div>
            <h1 className='header_title'>Консилиум – помощь в лечении онкобольных</h1>
         </header>

         <form action='' className='form' onSubmit={handleFormSubmit}>
            <div className='input_container'>
               <input
                  type='text'
                  value={query}
                  placeholder='Введите запрос'
                  className='input_container_field'
                  onChange={handleIputChange}
               />
               <button className='input_btn'>Сгенерировать</button>
            </div>
         </form>

         <div className='textarea_container'>
            <label htmlFor='textarea' className='textarea_label'>
               Текст
            </label>
            <textarea
               id='textarea'
               rows={15}
               defaultValue={response}
               className='textarea_field'
               disabled
            ></textarea>
         </div>
      </section>
   );
}

export default App;
