import './style.css'
import Alpine from 'alpinejs'

window.Alpine = Alpine

const SERVICE_URL = 'https://olnhngr0k9.execute-api.us-west-1.amazonaws.com/api/generate'

Alpine.data('numbersForm', () => ({
  isLoading: false,
  isSubmitted: false,
  formData: {
    company_name: '',
    num_employees: null,
    revenue: null,
    lucky_number: null,
    zipcode: null
  },
  formMessage: '',
  fileUrl: null,
  submitForm() {
    this.isLoading = true;
    this.formMessage = ''
    fetch(SERVICE_URL, {
      method: 'POST',
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
      body: JSON.stringify(this.formData)
    })
      .then((response) => response.json())
      .then((data) => {
        this.isSubmitted = true;
        this.resetForm()
        this.fileUrl = data.file_url;
      })
      .catch(() => {
        this.formMessage = 'Something went wrong.'
      })
      .finally(() => {
        this.isLoading = false;
      })
  },
  resetForm() {
    this.formData.company_name = ''
    this.formData.num_employees = null
    this.formData.revenue = null
    this.formData.lucky_number = null
    this.formData.zipcode = null
  },
  get isFormComplete() {
    return Object.values(this.formData).every(value => value)
  }
}))

Alpine.start()
