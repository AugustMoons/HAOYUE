document.addEventListener('DOMContentLoaded', function () {
    const themeToggleBtn = document.querySelector('.switch .input');
    const body = document.body;
    const header = document.querySelector('.header');
	const userico = document.querySelector('.userico');
	const container = document.querySelector('.container');
	const containeruser = document.querySelector('.container-user');
	const containerimport = document.querySelector('.container-import');
	const containerdata1 = document.querySelector('.container-data1');
	const containerdata2 = document.querySelector('.container-data2');
	const containerdata3 = document.querySelector('.container-data3');
	const mainbacck = document.querySelector('.main_back');
	const text = document.querySelector('.text');

            themeToggleBtn.addEventListener('change', function () {
                body.style.backgroundColor = themeToggleBtn.checked ? 'var(--background-color-dark)' : 'var(--background-color-light)';
                header.style.backgroundColor = themeToggleBtn.checked ? 'var(--background-color-dark)' : 'var(--background-color-light)';
				userico.style.backgroundColor = themeToggleBtn.checked ? 'var(--background-color-dark)' : 'var(--background-color-light)';
				container.style.backgroundColor = themeToggleBtn.checked ? 'var(--background-color-dark)' : 'var(--background-color-light)';
				containeruser.style.backgroundColor = themeToggleBtn.checked ? 'var(--background-color-dark)' : 'var(--background-color-light)';
				containerimport.style.backgroundColor = themeToggleBtn.checked ? 'var(--background-color-dark)' : 'var(--background-color-light)';
				containerdata1.style.backgroundColor = themeToggleBtn.checked ? 'var(--background-color-dark)' : 'var(--background-color-light)';
				containerdata2.style.backgroundColor = themeToggleBtn.checked ? 'var(--background-color-dark)' : 'var(--background-color-light)';
				containerdata3.style.backgroundColor = themeToggleBtn.checked ? 'var(--background-color-dark)' : 'var(--background-color-light)';
				mainbacck.style.boxShadow = themeToggleBtn.checked ? 'var(--background-color-dark)' : 'var(--background-color-light1)';
				mainbacck.style.background = themeToggleBtn.checked ? 'var(--background-color-dark)' : 'var(--background-color-light2)';
				text.style.color = themeToggleBtn.checked ? 'var(--color-dark)' : 'var(--color-light)';
            });
        });