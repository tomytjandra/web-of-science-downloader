import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import math
import time

# ---------- PAGE CONFIGURATION

st.set_page_config(
    page_title='Web of Science Downloader',
    layout='wide')
        
st.markdown(
    """
    <style>            
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .footer {
        position: fixed;
        display: block;
        width: 100%;
        bottom: 0;
        color: rgba(49, 51, 63, 0.4);
    }
    a:link , a:visited{
        color: rgba(49, 51, 63, 0.4);
        background-color: transparent;
        text-decoration: underline;
    }
    </style>
    <div class="footer">
        <p>
            Developed with ❤ by 
            <a href="https://github.com/tomytjandra" target="_blank">
            Tomy Tjandra
            </a>
        </p>
    </div>
    """, unsafe_allow_html=True)

def main():
    url = st.text_input("Enter URL")

    if st.button("Start"):
        # open browser
        options = Options()
        # options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        driver = webdriver.Chrome(options=options)
        driver.maximize_window()

        try:
            # access url
            driver.get(url)

            # close popup notifications
            onetrust_banner = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.ID, "onetrust-close-btn-container"))
            )
            onetrust_banner.click()
            tour_close_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "[aria-label='Close this tour']"))
            )
            tour_close_button.click()

            # get the number of results
            n_result = driver.find_element_by_class_name("brand-blue").text  # get the text
            n_result = int(n_result.replace(",", ""))  # remove comma and change to integer

            # determine number of iterations required
            n_iter = math.ceil(n_result / 500)
            # st.info(f"{n_result} RESULTS FOUND")
            # st.info(f"{n_iter} FILES WILL BE DOWNLOADED")

            progress_bar = st.progress(0)
            TIME_GAP = 1
            for iter in range(n_iter):
                # progress bar
                progress_text = f"Downloading {iter+1} out of {n_iter} file(s). Please don't close the browser."
                progress_bar.progress(iter/n_iter, text=progress_text)

                # click Export
                time.sleep(TIME_GAP)
                driver.find_element_by_tag_name("app-export-menu").click()

                # choose Plain text file
                time.sleep(TIME_GAP)
                driver.find_element_by_css_selector("[aria-label='Plain text file']").click()

                # choose the second radio button
                time.sleep(TIME_GAP)
                driver.find_element_by_css_selector("[for='radio3-input']").click()

                # input from and to
                time.sleep(TIME_GAP)
                from_rec, to_rec = 500*iter+1, 500*(iter+1)
                input_el_from, input_el_to = driver.find_elements_by_class_name("mat-input-element")
                input_el_from.clear()
                input_el_from.send_keys(from_rec)
                input_el_to.clear()
                input_el_to.send_keys(to_rec)

                # click dropdown
                time.sleep(TIME_GAP)
                driver.find_element_by_class_name("dropdown").click()

                # choose Full Record and Cited References
                time.sleep(TIME_GAP)
                driver.find_element_by_css_selector("[title='Full Record and Cited References']").click()

                # click Export
                time.sleep(TIME_GAP)
                for btn in driver.find_elements_by_tag_name('button'):
                    if btn.text == 'Export':
                        btn.click()
                        break

                # Wait until the popup dialog is not visible
                wait = WebDriverWait(driver, 60)
                while True:
                    try:
                        wait.until_not(EC.visibility_of_element_located((By.CLASS_NAME, "window")))
                        break
                    except TimeoutException:
                        print("Timed out waiting for popup dialog to disappear, retrying...")

                st.success(f"SUCCESS DOWNLOADED FROM {from_rec} TO {to_rec}")
        
        except Exception as e:
            st.error(f"An error occurred: {e}")
            driver.quit()

if __name__ == "__main__":
    main()