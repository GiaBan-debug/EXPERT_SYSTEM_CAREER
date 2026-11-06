/**
 * FORM VALIDATION HELPER
 * Kiểm tra các trường dữ liệu điểm số, thông tin học sinh
 */

const Validator = {
  isValidName(name) {
    return name && name.trim().length >= 2;
  },

  isValidScore(val) {
    const num = parseFloat(val);
    return !isNaN(num) && num >= 0 && num <= 10;
  },

  validateStudentStep(formElement) {
    let isValid = true;
    const nameInput = formElement.querySelector('#studentName');
    const classInput = formElement.querySelector('#studentGrade');

    if (!nameInput.value.trim()) {
      this.markInvalid(nameInput, "Vui lòng nhập họ và tên của học sinh");
      isValid = false;
    } else {
      this.clearInvalid(nameInput);
    }

    if (!classInput.value) {
      this.markInvalid(classInput, "Vui lòng chọn khối lớp học");
      isValid = false;
    } else {
      this.clearInvalid(classInput);
    }

    return isValid;
  },

  markInvalid(element, msg) {
    element.classList.add('is-invalid');
    const feedback = element.parentElement.querySelector('.invalid-feedback');
    if (feedback) feedback.textContent = msg;
  },

  clearInvalid(element) {
    element.classList.remove('is-invalid');
  }
};
