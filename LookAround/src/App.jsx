import { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
   const [query, setQuery] = useState(''); /** поисковый запрос */
   const [response, setResponse] = useState(''); /** ответ с сервера */
   const [isLoading, setIsLoading] = useState(false); // добавляем состояние загрузки
   const [error, setError] = useState(''); // добавляем состояние ошибки

   /** функция-обработчик поискового поля */
   const handleIputChange = ({ target }) => setQuery(target.value);

   /** функция отправки поискового запроса */
   const handleFormSubmit = async (e) => {
      /** предотвращаем перезагрузку страницы */
      e.preventDefault();

      setIsLoading(true); // начинаем загрузку
      setError(''); // очищаем ошибки

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
         setError('Ошибка при генерации ответа'); // устанавливаем ошибку
      } finally {
         setIsLoading(false); // заканчиваем загрузку
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
                  disabled={isLoading} // блокируем во время загрузки
               />
               <button
                  className='input_btn'
                  disabled={isLoading} // блокируем во время загрузки
               >
                  {isLoading ? 'Генерация...' : 'Сгенерировать'}
               </button>
            </div>
         </form>

         {/* Блок ошибки */}
         {error && (
            <div className='error-message'>
               ❌ {error}
            </div>
         )}

         <div className='textarea_container'>
            <label htmlFor='textarea' className='textarea_label'>
               Текст
            </label>

            {/* Показываем спинер внутри textarea контейнера */}
            {isLoading ? (
               <div className="loading-area">
                  <div className="loading-spinner"></div>
                  <p className="loading-text">Идет генерация ответа...</p>
               </div>
            ) : (
               <textarea
                  id='textarea'
                  rows={15}
                  value={response}
                  className='textarea_field'
                  disabled
                  placeholder={response ? '' : 'Здесь появится ответ'}
               ></textarea>
            )}
         </div>
      </section>
   );
}

export default App;