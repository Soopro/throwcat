angular.module 'throwCat'

.constant 'ConfigAgent',

  promo_types: [
    {
      key: 0
      name: 'Generic'
    }
    {
      key: 1
      name: 'Coupon'
    }
    {
      key: 2
      name: 'Ticket'
    }
    {
      key: 3
      name: 'Redeem'
    }
    {
      key: 4
      name: 'Gift Card'
      upper: true
    }
    {
      key: 5
      name: 'Loyalty Card'
      upper: true
    }
  ]

