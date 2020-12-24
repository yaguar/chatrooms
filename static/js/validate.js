const validate = values => {
  const errors = {}
   
  if (!values.first_name) {
    errors.first_name = 'Это обязательное поле!'
  } else if (values.first_name.length > 20) {
    errors.first_name = 'Не больше 20 сомволов!'
  } else if (!/^[A-Za-zА-Яа-яЁё]+$/i.test(values.first_name)) {
    errors.first_name = 'Некорректные символы!'
  }


  if (!values.last_name) {
    errors.last_name = 'Это обязательное поле!'
  } else if (values.last_name.length > 20) {
    errors.last_name = 'Не больше 20 символов!'
  } else if (!/^[A-Za-zА-Яа-яЁё]+$/i.test(values.last_name)) {
    errors.last_name = 'Некорректные символы!'
  }


  if (!values.phone) {
    errors.phone = 'Это обязательное поле!'
  } else if (!/^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$/i.test(values.phone)) {
    errors.phone = 'Некорректный номер!'
  }
  return errors
}

export default validate;
