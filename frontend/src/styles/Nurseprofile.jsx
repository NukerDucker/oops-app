import { useState } from "react";
import "../styles/Global.css";
import "../styles/Nurseprofile.css";
import * as React from 'react';


const Nurseprofile = () => {
    return (
      <div className="ContainerPage">
        <div className="profile-page-card-parent">
          
          <div className="profile-page-card-child">
            <div className="profile-page-card-child-left">
              <img src="Med-removebg.png" className="logo"></img>
              <p>Nurse</p>
              <img src="Profile-Icon.png" className="profile-icon"></img>
              <p>Nuttawee W.</p>
              <p>nhowthailand@gmail.com</p>
            </div>
            <div className="VL1"></div>
            <div className="profile-page-card-child-right">
              
              <div className="profile-page-card-child-right-top">
                <p className="welcome-text">Welcome back!, Nuttawee</p>
                <div className="search-bar">
                  <input name="search" type="text" placeholder="type to search"></input>
                  <button type="summit"><img src="search-icon.png"></img></button>
                </div>
              </div>
              
              <div className="annoucement-box">
              <div id="slider">
   
                <input type="radio" name="slider" id="slide1" checked></input>
                <input type="radio" name="slider" id="slide2"></input>
                <input type="radio" name="slider" id="slide3"></input>
                <input type="radio" name="slider" id="slide4"></input>
                  
                <div id="slides">
                    <div class="inner">
                      <div class="slide slide_1">
                         <div class="slide-content">
                            <h2>Slide 1</h2>
                            <p>Content for Slide 1</p>
                         </div>
                      </div>
                      <div class="slide slide_2">
                         <div class="slide-content">
                             <h2>Slide 2</h2>
                            <p>Content for Slide 2</p>
                         </div>
                      </div>
                      <div class="slide slide_3">
                         <div class="slide-content">
                            <h2>Slide 3</h2>
                            <p>Content for Slide 3</p>
                         </div>
                      </div>
                      <div class="slide slide_4">
                         <div class="slide-content">
                            <h2>Slide 4</h2>
                            <p>Content for Slide 4</p>
                          </div>
                      </div>
                   </div>
                </div>
                  
                <div id="bullets">
                   <label for="slide1"></label>
                   <label for="slide2"></label>
                   <label for="slide3"></label>
                   <label for="slide4"></label>
                </div>
              </div>
              </div>

              <div className="profile-page-card-child-right-bottom">
                <div className="profile-page-card-child-right-bottom-left">
                  <h2>Daily Tasks</h2>
                  <div className="dailytask-box">
                      <h2>Hello</h2>
                      <p>Somewhere</p>
                  </div>
                  <div className="dailytask-box">
                  <h2>Hello</h2>
                  <p>Somewhere</p>
                  </div>
                </div>
                <div className="profile-page-card-child-right-bottom-right">
                <h2>Weekly Tasks</h2>
                <div className="dailytask-box">
                      <h2>Hello</h2>
                      <p>Somewhere</p>
                  </div>
                  <h2>Emergency</h2>
                <div className="dailytask-box">
                      <h2>Hello</h2>
                      <p>Somewhere</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <div className="profile-page-calendar">
            <div className="profile-page-calendar-top">
            <h2>Calendar</h2>
            <img src="notify.png"></img>
            </div>
            <div className="calendar">
              <div className="date">
                <p>Mar 12, 2025</p>
              </div>
              <div className="calendar-time">
              <div className="time">
                <p>10:00</p>
                <h2></h2>
                <h3>Do something</h3>
              </div>
              <div className="time">
                <p>10:00</p>
                <h2></h2>
                <h3>Do something</h3>
              </div>
                
              </div>

              <div className="date">
                <p>Mar 12, 2025</p>
              </div>
              <div className="calendar-time">
              <div className="time">
                <p>10:00</p>
                <h2></h2>
                <h3>Do something</h3>
              </div>
              <div className="time">
                <p>10:00</p>
                <h2></h2>
                <h3>Do something</h3>
              </div>
                
              </div>

              <div className="date">
                <p>Mar 12, 2025</p>
              </div>
              <div className="calendar-time">
              <div className="time">
                <p>10:00</p>
                <h2></h2>
                <h3>Do something</h3>
              </div>
              <div className="time">
                <p>10:00</p>
                <h2></h2>
                <h3>Do something</h3>
              </div>
                
              </div>

              
             
              
            </div>
            


          </div>
          
        </div>
      </div>
      
    )
}
export default Nurseprofile