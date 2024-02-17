import React, { useEffect, useState } from 'react'
import Example from '../charts/Calendar.js'
import {
  CButton,
  CButtonGroup,
  CCard,
  CCardBody,
  CDropdown,
  CDropdownItem,
  CDropdownMenu,
  CDropdownToggle,
  CCardHeader,
  CCol,
  CRow,
} from '@coreui/react'
import { CChartLine } from '@coreui/react-chartjs'
import { getStyle, hexToRgba } from '@coreui/utils'
import { useDispatch, useSelector } from 'react-redux'
import { getPlayerData } from '../../redux/data/dataPlayerSlice'


const Dashboard = () => {
  const dispatch = useDispatch()
  const { players } = useSelector((state) => state.players)
  const { data } = useSelector((state) => state.data)
  const { dataPlayer } = useSelector((state) => state.dataPlayer)
  const [dataState, setIndex] = useState('')
  const [selected, setSelected] = useState('')

  const matchday = ["2021-08-14", "2021-08-21","2021-08-29", 
    "2021-09-12", "2021-09-17", "2021-09-25", "2021-10-02", "2021-10-16",
    "2021-10-23", "2021-10-31", "2021-11-07", "2021-11-21", "2021-11-27", 
    "2021-11-30", "2021-12-05","2021-12-11", "2021-12-14", "2021-12-18", 
    "2022-02-23", "2022-03-10", "2022-01-02", "2022-01-16","2022-01-22", 
    "2022-02-09", "2022-02-12", "2022-02-20", "2022-02-26", "2022-03-05", 
    "2022-03-13","2022-03-18", "2022-04-02", "2022-04-09", "2022-05-11", 
    "2022-04-25", "2022-04-30", "2022-05-08", "2022-05-15", "2022-05-22", 
    "2021-07-27", "2021-07-28", "2021-07-30", "2021-07-31", "2021-08-04",
    "2021-08-07", "2021-08-24", "2021-08-07", "2021-09-21", "2021-10-26", "2022-01-09"]

  useEffect(() => {
    players.forEach(element => {
      if (Object.values(element).indexOf(dataState) > -1) {
        setSelected(element.playerName)
      }
    });
    if (dataState !== '') {
      dispatch(getPlayerData(dataState))
    }
  }, [dataState, players, dispatch])

  const [chartMode, setChartMode] = useState("Overview");

  const toggle = () => {
    if (chartMode === "Overview") {
      setChartMode("Detailed")
    } else {
      setChartMode("Overview")
    }
  }
  
  let labels_month = {}
  if (dataPlayer !== undefined) {
    dataPlayer.forEach(element => {
      let data = JSON.parse(element['data'])
      data.forEach((element) => {
        let date = element[0]
        let date_obj = Date.parse(date)
        var monthName;
        if (chartMode === "Overview")
          monthName = new Intl.DateTimeFormat("en-US", { month: "long" }).format;
        else
          monthName = new Intl.DateTimeFormat("en-US").format;

        var longName = monthName(date_obj);
        if (longName in labels_month) {
          labels_month[longName].push(parseInt(element[1]))
        } else {
          labels_month[longName] = [parseInt(element[1])]
          labels_month[longName].push(parseInt(element[1]))
        }
      })
    });
  }
  let matchday_data = {}
  matchday.forEach((element) => {
    let date = element
    let date_obj = Date.parse(date)
    var monthName;

    if (chartMode === "Overview") {
      monthName = new Intl.DateTimeFormat("en-US", { month: "long" }).format;
      var longName = monthName(date_obj);
      if (longName in matchday_data) {
        matchday_data[longName] += 1
      } else {
        matchday_data[longName] = 1
      }
    } else {
      monthName = new Intl.DateTimeFormat("en-US").format;
      var longName = monthName(date_obj);
      if (longName in matchday_data) {
        matchday_data[longName] += 1
      } else {
        matchday_data[longName] = 1
      }
    }
  })
  console.log(matchday_data)

  let line_data = []
  if (labels_month) {
    Object.keys(labels_month).forEach((element) => {
      line_data.push(labels_month[element])
    })
  }

  let bar_labels = []
  if (matchday_data) {
    Object.keys(matchday_data).forEach((element) => {
      bar_labels.push(matchday_data[element])
    })
  }


  return (
    <>
      <div >
        <CDropdown>
          <CDropdownToggle color="secondary">Select Player</CDropdownToggle>
          <CDropdownMenu>
            {players.map((color, index) => (
              <CDropdownItem onClick={() => setIndex(color.playerId)} >{color.playerName}</CDropdownItem>
            ))}
          </CDropdownMenu>
        </CDropdown>
      </div>
      <br />

      <div className="row">
      </div>
      <CCard className="mb-4">
        <CCardBody>
          <CRow>
            <CCol sm={5}>
              <h4 id="traffic" className="card-title mb-0">
                {selected} Performance Overview (Fatigue Levels)
              </h4>
              <div className="small text-medium-emphasis">{ }</div>
            </CCol>
            <CCol sm={7} className="d-none d-md-block">

              <CButtonGroup className="float-end me-3">
                {['Overview', 'Detailed'].map((value) => (
                  <CButton
                    color="outline-secondary"
                    key={value}
                    className="mx-0"
                    active={value === chartMode}
                    onClick={toggle}
                  >
                    {value}
                  </CButton>
                ))}
              </CButtonGroup>
            </CCol>
          </CRow>
          <CChartLine
            style={{ height: '300px', marginTop: '40px' }}
            data={{
              labels: Object.keys(labels_month),
              datasets: [
                {
                  label: 'Fatigue Level',
                  backgroundColor: hexToRgba(getStyle('--cui-info'), 10),
                  borderColor: getStyle('--cui-info'),
                  pointHoverBackgroundColor: getStyle('--cui-info'),
                  borderWidth: 2,
                  data: line_data,
                  fill: true,
                },
                {
                  type: 'bar',
                  label: 'Match Days (& Count)',
                  data: bar_labels
                }
              ],
            }}
            options={{
              maintainAspectRatio: false,
              plugins: {
                legend: {
                  display: true,
                },
              },
              scales: {
                x: {
                  grid: {
                    drawOnChartArea: false,
                  },
                },
                y: {
                  ticks: {
                    beginAtZero: true,
                    maxTicksLimit: 5,
                    stepSize: Math.ceil(250 / 5),
                    max: 250,
                  },
                },
              },
              elements: {
                line: {
                  tension: 0.4,
                },
                point: {
                  radius: 0,
                  hitRadius: 10,
                  hoverRadius: 4,
                  hoverBorderWidth: 3,
                },
              },
            }}
          />
        </CCardBody>
      </CCard>
      <CRow>
        <CCol xs>
          <CCard className="mb-4">
            <CCardHeader>Heatmap {' & '} Comperative</CCardHeader>
            <CCardBody>
              <CRow>
                <Example data1={dataPlayer} type='dataPlayer' />
              </CRow>
              <br />
              <br />
              <CRow>
                <Example data1={data} type='totalData' />
              </CRow>
            </CCardBody>
          </CCard>
        </CCol>
      </CRow>

    </>
  )
}

export default Dashboard
