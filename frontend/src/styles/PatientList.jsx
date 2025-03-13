import "../styles/Global.css";
import "../styles/PatientList.css";
import * as React from 'react';


const PatientList = () => {
    return (
      <div className="ContainerPage">
        <div className="profile-page-card-parent">
          
          <div className="profile-page-card-child">
            <div className="profile-page-card-child-left">
              <img src="Med-removebg.png" className="logo"></img>
              <p>Nurse</p>
              <svg width="108" height="108" viewBox="0 0 108 108" fill="none" xmlns="http://www.w3.org/2000/svg">
<rect x="0.929932" y="0.585938" width="106.533" height="106.533" rx="53.2666" fill="#EADDFF"/>
<path fill-rule="evenodd" clip-rule="evenodd" d="M70.1771 43.1992C70.1771 52.0247 63.0226 59.1792 54.1971 59.1792C45.3717 59.1792 38.2172 52.0247 38.2172 43.1992C38.2172 34.3737 45.3717 27.2192 54.1971 27.2192C63.0226 27.2192 70.1771 34.3737 70.1771 43.1992ZM64.8505 43.1992C64.8505 49.0829 60.0808 53.8525 54.1971 53.8525C48.3135 53.8525 43.5438 49.0829 43.5438 43.1992C43.5438 37.3155 48.3135 32.5459 54.1971 32.5459C60.0808 32.5459 64.8505 37.3155 64.8505 43.1992Z" fill="#4F378A"/>
<path d="M54.1972 67.1692C36.9537 67.1692 22.2619 77.3655 16.6654 91.6506C18.0288 93.0044 19.4649 94.2849 20.9676 95.4858C25.135 82.3706 38.2084 72.4958 54.1972 72.4958C70.1859 72.4958 83.2594 82.3707 87.4268 95.4859C88.9294 94.285 90.3656 93.0044 91.7289 91.6506C86.1324 77.3655 71.4406 67.1692 54.1972 67.1692Z" fill="#4F378A"/>
</svg>

              <p>Nuttawee W.</p>
              <p>nhowthailand@gmail.com</p>
            </div>
            <div className="VL1"></div>
            <div className="profile-page-card-child-right">
              
              <div className="profile-page-card-child-right-top">
                <h2>Patients list:</h2>
                <div className="search-bar">
                  <input name="search" type="text" placeholder="type to search"></input>
                  <button type="summit"><img src="search-icon.png"></img></button>
                </div>
                <div className="regist-button">
                <button ><img src="plus.png"></img>Register Patient</button>
                </div>
    
              </div>
              <div className="VL2"></div>
              <div className="title">
                    <h1>Name</h1>
                    <h2>ID</h2>
                    <h3>Phone</h3>
                </div>
              <div className="profile-page-card-child-right-bottom">
                <div className="patient-list">
                <div className="patient-list-child">
                <img src="Profile-Icon.png" className="profile-icon"></img>
                <span>
                  <h1>Pannatat Sriyam</h1>
                  <p>Gender: Male</p>
                  <p>Age: 19</p>
                </span>
                <h2>12345</h2>
                <h3>091-748-xxxx</h3>
                <div className="container">
                <div className="btn-warpper">
                  <button>
                    <svg width="7" height="24" viewBox="0 0 7 24" fill="none" xmlns="http://www.w3.org/2000/svg">
<ellipse cx="3.5" cy="20.6713" rx="2.8287" ry="3.5" transform="rotate(-90 3.5 20.6713)" fill="#A9A9A9"/>
<ellipse cx="3.5" cy="2.82877" rx="2.8287" ry="3.5" transform="rotate(-90 3.5 2.82877)" fill="#A9A9A9"/>
<ellipse cx="3.5" cy="11.75" rx="2.61111" ry="3.5" transform="rotate(-90 3.5 11.75)" fill="#A9A9A9"/>
</svg>
                    <span>Edit</span>
                  </button>
                  <div className="dropdown">
                      <ul>
                          <li>
                              <a href="#">
                                  <span>PatientRecord</span>
                              </a>
                          </li>
                          <li>
                              <a href="#">
                                  <span>Appointment</span>
                              </a>
                          </li>
                          <li>
                              <a href="#">
                                  <span>LabTest</span>
                              </a>
                          </li>
                          <li>
                              <a href="#">
                                  <span>PrescribeMedicine</span>
                              </a>
                          </li>
                          <li>
                              <a href="#">
                                  <span>Invoice</span>
                              </a>
                          </li>
                      </ul>
                  </div>
                  
                </div>
                </div>

                
                </div>
                
                
                
                </div>

              </div>
              
              

              
            </div>
          </div>
          
          
          
        </div>
      </div>
      
    )
}
export default PatientList