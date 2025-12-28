generateCapthca();

function generateCapthca() {
	fetch('/captcha/generate')   // proxy endpoint/
		// fetch('generate')

		.then(response => {
			const captchaId = response.headers.get('Captcha-ID');
			document.getElementById('captcha_id').value = captchaId;
			return response.blob();
		})
		.then(blob => {
			const imageUrl = URL.createObjectURL(blob);
			document.getElementById('captcha').src = imageUrl;
		})
		.catch(error => console.error("Error loading CAPTCHA:", error));
}

const form = document.getElementById('captchaForm');
const capInputField = document.getElementById('capInput');


form.addEventListener('submit', function (e) {
	e.preventDefault();
	const formData = new FormData(form);
	const plainData = {};
	formData.forEach((value, key) => {
		plainData[key] = value;
	});
	fetch("/devMode", { cache: "no-store" })
		.then(res => res.json())
		.then(({ devMode}) => {
			console.log("response : ", devMode)


			if (devMode) {
				// ✅ Dev mode → skip captcha
				submitLogin(formData);
			}
			else {

				fetch('/captcha/validate', {   // 	proxy endpoint
					method: 'POST',
					headers: {
						"Content-Type": "application/json"
					},
					body: JSON.stringify(plainData)
				})
					.then(res => res.json())
					.then(data => {
						if (data.success) {
							submitLogin(formData);
						} else {
							const msg = document.getElementById('result');
							const inputFiled = document.getElementById('capInput');
							msg.textContent = data.message;
							msg.classList.add('error');
							inputFiled.classList.add('borderError');
							capInputField.value = "";
							generateCapthca();
						}
					})
					.catch(err => console.error("Error:", err));
			}

		
			// else{
			// 	console.log("Else is running");
			// 	fetch('/login', {

			// 					method: 'POST',
			// 					body: formData   // send original login fields (username, password, etc.)
			// 				})
			// 					.then(res => {
			// 						if (res.redirected) {
			// 							window.location.href = res.url;
			// 						} else {
			// 							return res.text().then(html => {
			// 								document.body.innerHTML = html;
			// 							});
			// 						}
			// 					});
			// }
	})
});


function submitLogin(formData) {
	fetch('/login', {
		method: 'POST',
		body: formData
	})
		.then(res => {
			if (res.redirected) {
				window.location.href = res.url;
			} else {
				return res.text().then(html => {
					document.body.innerHTML = html;
				});
			}
		});
}