/**
 * CURLIQUE — Core JavaScript Interactivity
 * Strictly Vanilla JS (No unapproved frameworks)
 */

document.addEventListener('DOMContentLoaded', function () {
  // 1. Progressive Quiz Wizard Navigation
  const quizForm = document.getElementById('curlQuizForm');
  if (quizForm) {
    const steps = document.querySelectorAll('.quiz-step-card');
    const progressBar = document.getElementById('quizProgressBar');
    const currentStepText = document.getElementById('currentStepNum');
    const prevBtn = document.getElementById('quizPrevBtn');
    const nextBtn = document.getElementById('quizNextBtn');
    const submitBtn = document.getElementById('quizSubmitBtn');
    let currentStep = 0;

    function showStep(stepIndex) {
      steps.forEach((step, idx) => {
        if (idx === stepIndex) {
          step.classList.add('active');
        } else {
          step.classList.remove('active');
        }
      });

      // Update progress bar
      const progressPercent = Math.round(((stepIndex + 1) / steps.length) * 100);
      if (progressBar) {
        progressBar.style.width = progressPercent + '%';
        progressBar.setAttribute('aria-valuenow', progressPercent);
      }
      if (currentStepText) {
        currentStepText.textContent = stepIndex + 1;
      }

      // Prev button visibility
      if (prevBtn) {
        if (stepIndex === 0) {
          prevBtn.style.display = 'none';
        } else {
          prevBtn.style.display = 'inline-block';
        }
      }

      // Next vs Submit button
      if (stepIndex === steps.length - 1) {
        if (nextBtn) nextBtn.style.display = 'none';
        if (submitBtn) submitBtn.style.display = 'inline-block';
      } else {
        if (nextBtn) nextBtn.style.display = 'inline-block';
        if (submitBtn) submitBtn.style.display = 'none';
      }

      window.scrollTo({ top: quizForm.offsetTop - 80, behavior: 'smooth' });
    }

    if (nextBtn) {
      nextBtn.addEventListener('click', function () {
        // Validation for the current step
        const currentCard = steps[currentStep];
        const inputs = currentCard.querySelectorAll('input');
        let answered = false;

        if (inputs.length > 0) {
          inputs.forEach(input => {
            if (input.type === 'radio' && input.checked) answered = true;
            if (input.type === 'checkbox' && input.checked) answered = true;
          });
        } else {
          answered = true;
        }

        if (!answered) {
          alert('Please make a selection to continue to the next step.');
          return;
        }

        if (currentStep < steps.length - 1) {
          currentStep++;
          showStep(currentStep);
        }
      });
    }

    if (prevBtn) {
      prevBtn.addEventListener('click', function () {
        if (currentStep > 0) {
          currentStep--;
          showStep(currentStep);
        }
      });
    }

    showStep(0);
  }

  // 2. City Selection Delivery Fee Live Update in Checkout
  const citySelect = document.getElementById('citySelect');
  const deliveryFeeDisplay = document.getElementById('deliveryFeeDisplay');
  const totalAmountDisplay = document.getElementById('totalAmountDisplay');
  const subtotalInput = document.getElementById('orderSubtotalVal');

  if (citySelect && deliveryFeeDisplay && totalAmountDisplay && subtotalInput) {
    const subtotal = parseFloat(subtotalInput.value) || 0;

    function updateDeliveryFee() {
      const selectedCity = citySelect.value;
      let fee = 180.0; // Outside valley
      if (['Kathmandu', 'Lalitpur', 'Bhaktapur'].includes(selectedCity)) {
        fee = 100.0; // Kathmandu Valley
      }
      deliveryFeeDisplay.textContent = 'NPR ' + fee.toFixed(2);
      const total = subtotal + fee;
      totalAmountDisplay.textContent = 'NPR ' + total.toFixed(2);
    }

    citySelect.addEventListener('change', updateDeliveryFee);
  }

  // 3. Auto-dismiss alerts after 5 seconds
  const autoAlerts = document.querySelectorAll('.alert-dismissible');
  autoAlerts.forEach(function (alert) {
    setTimeout(function () {
      const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
      if (bsAlert) bsAlert.close();
    }, 6000);
  });
});
