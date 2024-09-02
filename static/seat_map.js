document.addEventListener('DOMContentLoaded', function() {
            const seatData = JSON.parse(document.getElementById('seat_data').textContent);
            const app = Vue.createApp({
                data() {
                    return {
                        business_seats: seatData.business_seats,
                        first_class_seats: seatData.first_class_seats,
                        economy_seats: seatData.economy_seats,
                        seats_per_business_row: seatData.seats_per_business_row,
                        seats_per_first_class_row: seatData.seats_per_first_class_row,
                        seats_per_economy_row: seatData.seats_per_economy_row,
                        selectedSeats: []
                    };
                },
                methods: {
                    toggleSeat(seat_id) {
                        const index = this.selectedSeats.indexOf(seat_id);
                        const seat = [...this.business_seats, ...this.first_class_seats, ...this.economy_seats].find(s => s.id === seat_id);
                        if(!seat.booked){
                            if (index === -1) {
                                this.selectedSeats.push(seat_id);
                            } else {
                                this.selectedSeats.splice(index, 1);
                            }
                            console.log(this.selectedSeats);
                        }
                    },
                    seatClass(seat) {
                        let seatClass;
                        if (seat.booked) {
                            seatClass = 'seat reserved';
                        } else if (this.selectedSeats.includes(seat.pk)) {
                            seatClass = 'seat selected';
                        } else {
                            seatClass = 'seat ' + seat.get_flight_class_display.toLowerCase().replace(" ", "_");
                        }
                        return seatClass;
                    },
                    AddRebooking(seat_id) {
                        this.toggleSeat(seat_id);
                    }
                },
                loadPage(){
                    const url = event.target.getAttribute('data-url');
                    
                }
            });

            app.mount('#airplane');
        });